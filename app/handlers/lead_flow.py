"""
Lead collection flow - FSM для пошагового сбора заявок.

Этот модуль реализует:
- Команду /new для создания новой заявки
- Пошаговый опрос (имя → телефон → email → описание)
- Валидацию каждого поля
- Preview заявки перед отправкой
- Редактирование полей
- Сохранение в БД и уведомление админу
"""
import re
import logging
from datetime import datetime
from typing import Optional

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import pytz

from app.config import DB_PATH, ADMIN_CHAT_ID, TIMEZONE
from app.db import get_user_language, save_lead, get_last_lead_by_user
from app.locales import get_text, format_text
from app.keyboards import (
    get_confirmation_keyboard,
    get_edit_keyboard,
    get_skip_keyboard,
    get_confirm_data_keyboard,
    get_files_keyboard,
    get_main_menu_keyboard,
    remove_keyboard
)
from app.states import LeadForm
from app.ai_enhancer import enhance_lead_description
import json

router = Router()
logger = logging.getLogger(__name__)


def validate_phone(phone: str) -> bool:
    """
    Валидация номера телефона.
    
    Правила:
    - Минимум 10 цифр в строке
    - Может содержать +, пробелы, дефисы, скобки
    
    Args:
        phone: Номер телефона для проверки
        
    Returns:
        True если телефон валиден, False иначе
    """
    # Извлекаем только цифры
    digits = re.sub(r'\D', '', phone)
    return len(digits) >= 10


def validate_email(email: str) -> bool:
    """
    Валидация email адреса.
    
    Простая проверка формата: text@text.text
    
    Args:
        email: Email для проверки
        
    Returns:
        True если email валиден, False иначе
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))


def format_lead_preview(
    full_name: str,
    phone: str,
    email: Optional[str],
    description: str,
    lang: str
) -> str:
    """
    Форматирование preview заявки для показа пользователю.
    
    Args:
        full_name: Имя пользователя
        phone: Номер телефона
        email: Email (может быть None)
        description: Описание проекта
        lang: Язык пользователя
        
    Returns:
        Отформатированный текст preview
    """
    email_display = email if email else get_text('email_not_provided', lang)
    
    return format_text(
        'preview_lead',
        lang,
        full_name=full_name,
        phone=phone,
        email=email_display,
        description=description
    )


async def send_admin_notification(
    bot,
    lead_id: int,
    tg_user_id: int,
    full_name: str,
    phone: str,
    email: Optional[str],
    description: str,
    lang: str,
    files: Optional[list] = None
) -> None:
    """
    Отправка уведомления админу о новой заявке.
    
    Описание проекта автоматически улучшается и структурируется
    перед отправкой администратору.
    
    Args:
        bot: Экземпляр бота
        lead_id: ID заявки в БД
        tg_user_id: Telegram ID пользователя
        full_name: Имя пользователя
        phone: Номер телефона
        email: Email (может быть None)
        description: Описание проекта
        lang: Язык заявки
    """
    try:
        # Получаем текущее время с учетом timezone
        tz = pytz.timezone(TIMEZONE)
        timestamp = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        
        email_display = email if email else get_text('email_not_provided', 'en')
        
        # 🤖 УЛУЧШАЕМ ОПИСАНИЕ С ПОМОЩЬЮ AI ENHANCER
        enhanced_description = enhance_lead_description(
            description=description,
            full_name=full_name,
            phone=phone,
            email=email,
            lang=lang,
            use_ai=False  # Пока без OpenAI, только структурирование
        )
        
        notification_text = (
            f"🧱 <b>{get_text('admin_notification', lang)}</b>\n\n"
            f"👤 <b>{full_name}</b>\n"
            f"🆔 Telegram ID: <code>{tg_user_id}</code>\n"
            f"📞 Phone: <code>{phone}</code>\n"
            f"✉️ Email: {email_display}\n\n"
            f"{'─' * 40}\n"
            f"{enhanced_description}\n"
            f"{'─' * 40}\n\n"
            f"💾 DB Lead ID: #{lead_id}\n"
            f"🌍 Language: {lang.upper()}\n"
            f"🕐 Time: {timestamp}"
        )
        
        # Отправляем основное уведомление
        await bot.send_message(
            chat_id=ADMIN_CHAT_ID,
            text=notification_text,
            parse_mode="HTML"
        )
        
        # Отправляем файлы если есть
        if files:
            for file_info in files:
                try:
                    if file_info['type'] == 'photo':
                        await bot.send_photo(
                            chat_id=ADMIN_CHAT_ID,
                            photo=file_info['file_id'],
                            caption=f"📎 Файл к заявке #{lead_id}"
                        )
                    elif file_info['type'] == 'document':
                        await bot.send_document(
                            chat_id=ADMIN_CHAT_ID,
                            document=file_info['file_id'],
                            caption=f"📎 Файл к заявке #{lead_id}"
                        )
                    elif file_info['type'] == 'video':
                        await bot.send_video(
                            chat_id=ADMIN_CHAT_ID,
                            video=file_info['file_id'],
                            caption=f"📎 Файл к заявке #{lead_id}"
                        )
                except Exception as file_error:
                    logger.error(f"Failed to send file to admin: {file_error}")
        
        logger.info(f"✅ Admin notification sent for lead #{lead_id}, user TG ID: {tg_user_id}, files: {len(files) if files else 0}")
        
    except Exception as e:
        logger.error(f"❌ FAILED to send admin notification to chat {ADMIN_CHAT_ID}: {e}", exc_info=True)
        logger.error(f"❌ Check that ADMIN_CHAT_ID={ADMIN_CHAT_ID} is correct and bot is not blocked")
        # Не пробрасываем ошибку - заявка уже сохранена в БД


@router.message(Command("new"))
async def cmd_new_lead(message: Message, state: FSMContext) -> None:
    """
    Обработчик команды /new - начало создания новой заявки.
    
    Проверяет есть ли у пользователя предыдущие заявки.
    Если есть - предлагает использовать старые данные.
    
    Args:
        message: Сообщение с командой /new
        state: FSM контекст для управления состоянием
    """
    user_id = message.from_user.id
    user_lang = get_user_language(user_id, DB_PATH) or 'en'
    
    # Очищаем предыдущее состояние если оно было
    await state.clear()
    
    # Проверяем есть ли предыдущие заявки
    last_lead = get_last_lead_by_user(user_id, DB_PATH)
    
    if last_lead:
        # У пользователя есть предыдущая заявка - предлагаем использовать данные
        email_display = last_lead['email'] if last_lead['email'] else get_text('email_not_provided', user_lang)
        
        confirm_text = format_text(
            'confirm_old_data',
            user_lang,
            full_name=last_lead['full_name'],
            phone=last_lead['phone'],
            email=email_display
        )
        
        await state.set_state(LeadForm.confirm_data)
        await state.update_data(
            language=user_lang,
            old_full_name=last_lead['full_name'],
            old_phone=last_lead['phone'],
            old_email=last_lead['email']
        )
        
        await message.answer(
            confirm_text,
            reply_markup=get_confirm_data_keyboard(user_lang)
        )
        logger.info(f"User {user_id} has previous leads, asking to confirm data")
    else:
        # Первая заявка пользователя - начинаем с имени
        await state.set_state(LeadForm.waiting_for_name)
        await state.update_data(language=user_lang)
        
        await message.answer(get_text('start_new_lead', user_lang))
        logger.info(f"User {user_id} started first lead form")


@router.callback_query(F.data.startswith("confirm_data:"))
async def process_data_confirmation(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработка подтверждения использования старых данных.
    
    Args:
        callback: Callback от кнопки подтверждения
        state: FSM контекст
    """
    data = await state.get_data()
    lang = data.get('language', 'en')
    action = callback.data.split(":")[1]  # use или change
    
    if action == "use":
        # Использовать старые данные - берем из state
        await state.update_data(
            full_name=data['old_full_name'],
            phone=data['old_phone'],
            email=data['old_email']
        )
        
        # Переходим сразу к описанию проекта
        await state.set_state(LeadForm.waiting_for_description)
        await callback.message.edit_text(get_text('ask_description', lang))
        logger.info(f"User {callback.from_user.id} reusing old data")
        
    else:  # change
        # Пользователь хочет изменить данные - начинаем заново
        await state.set_state(LeadForm.waiting_for_name)
        await callback.message.edit_text(get_text('start_new_lead', lang))
        logger.info(f"User {callback.from_user.id} changing data")
    
    await callback.answer()


@router.message(LeadForm.waiting_for_name)
async def process_name(message: Message, state: FSMContext) -> None:
    """
    Обработка ввода имени.
    
    Args:
        message: Сообщение с именем пользователя
        state: FSM контекст
    """
    data = await state.get_data()
    lang = data.get('language', 'en')
    
    full_name = message.text.strip()
    
    # Простая валидация: имя не должно быть пустым
    if not full_name or len(full_name) < 2:
        await message.answer(get_text('ask_name', lang))
        return
    
    # Сохраняем имя и переходим к телефону
    await state.update_data(full_name=full_name)
    await state.set_state(LeadForm.waiting_for_phone)
    
    await message.answer(get_text('ask_phone', lang))
    logger.debug(f"User {message.from_user.id} provided name: {full_name}")


@router.message(LeadForm.waiting_for_phone)
async def process_phone(message: Message, state: FSMContext) -> None:
    """
    Обработка ввода телефона с валидацией.
    
    Args:
        message: Сообщение с номером телефона
        state: FSM контекст
    """
    data = await state.get_data()
    lang = data.get('language', 'en')
    
    phone = message.text.strip()
    
    # Валидация телефона
    if not validate_phone(phone):
        await message.answer(get_text('invalid_phone', lang))
        return
    
    # Сохраняем телефон и переходим к email
    await state.update_data(phone=phone)
    await state.set_state(LeadForm.waiting_for_email)
    
    await message.answer(
        get_text('ask_email', lang),
        reply_markup=get_skip_keyboard(lang)
    )
    logger.debug(f"User {message.from_user.id} provided phone: {phone}")


@router.callback_query(F.data == "skip:email")
async def skip_email(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработка пропуска email (кнопка "Пропустить").
    
    Args:
        callback: Callback от кнопки пропуска
        state: FSM контекст
    """
    data = await state.get_data()
    lang = data.get('language', 'en')
    
    # Пропускаем email и переходим к описанию
    await state.update_data(email=None)
    await state.set_state(LeadForm.waiting_for_description)
    
    await callback.message.edit_text(get_text('ask_description', lang))
    await callback.answer()
    logger.debug(f"User {callback.from_user.id} skipped email")


@router.message(LeadForm.waiting_for_email)
async def process_email(message: Message, state: FSMContext) -> None:
    """
    Обработка ввода email с валидацией.
    
    Args:
        message: Сообщение с email
        state: FSM контекст
    """
    data = await state.get_data()
    lang = data.get('language', 'en')
    
    email = message.text.strip()
    
    # Валидация email
    if not validate_email(email):
        await message.answer(
            get_text('invalid_email', lang),
            reply_markup=get_skip_keyboard(lang)
        )
        return
    
    # Сохраняем email и переходим к описанию
    await state.update_data(email=email)
    await state.set_state(LeadForm.waiting_for_description)
    
    await message.answer(get_text('ask_description', lang))
    logger.debug(f"User {message.from_user.id} provided email: {email}")


@router.message(LeadForm.waiting_for_description)
async def process_description(message: Message, state: FSMContext) -> None:
    """
    Обработка ввода описания проекта с валидацией.
    
    Args:
        message: Сообщение с описанием
        state: FSM контекст
    """
    data = await state.get_data()
    lang = data.get('language', 'en')
    
    description = message.text.strip()
    
    # Валидация описания (минимум 10 символов)
    if len(description) < 10:
        await message.answer(get_text('description_too_short', lang))
        return
    
    # Сохраняем описание и переходим к файлам
    await state.update_data(description=description, files=[])
    await state.set_state(LeadForm.waiting_for_files)
    
    await message.answer(
        get_text('ask_files', lang),
        reply_markup=get_files_keyboard(lang)
    )
    logger.debug(f"User {message.from_user.id} provided description, asking for files")


@router.callback_query(F.data == "files:skip", LeadForm.waiting_for_files)
@router.callback_query(F.data == "files:done", LeadForm.waiting_for_files)
async def process_files_skip_or_done(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработка пропуска файлов или завершения загрузки.
    
    Args:
        callback: Callback от кнопки
        state: FSM контекст
    """
    data = await state.get_data()
    lang = data.get('language', 'en')
    
    # Переходим к preview
    await state.set_state(LeadForm.preview)
    
    files = data.get('files', [])
    files_info = f"\n📎 Файлов прикреплено: {len(files)}" if files else ""
    
    # Показываем preview
    preview_text = format_lead_preview(
        full_name=data['full_name'],
        phone=data['phone'],
        email=data.get('email'),
        description=data['description'],
        lang=lang
    ) + files_info
    
    await callback.message.edit_text(
        preview_text,
        reply_markup=get_confirmation_keyboard(lang)
    )
    await callback.answer()
    logger.debug(f"User {callback.from_user.id} finished with files, showing preview")


@router.message(LeadForm.waiting_for_files, F.photo | F.document | F.video)
async def process_file_upload(message: Message, state: FSMContext) -> None:
    """
    Обработка загрузки файла (фото, документ, видео).
    
    Args:
        message: Сообщение с файлом
        state: FSM контекст
    """
    data = await state.get_data()
    lang = data.get('language', 'en')
    files = data.get('files', [])
    
    # Определяем тип и получаем file_id
    if message.photo:
        file_id = message.photo[-1].file_id  # Берем самое большое фото
        file_type = 'photo'
    elif message.document:
        file_id = message.document.file_id
        file_type = 'document'
    elif message.video:
        file_id = message.video.file_id
        file_type = 'video'
    else:
        return
    
    # Сохраняем информацию о файле
    files.append({
        'type': file_type,
        'file_id': file_id
    })
    
    await state.update_data(files=files)
    
    await message.answer(
        get_text('file_received', lang),
        reply_markup=get_files_keyboard(lang)
    )
    logger.debug(f"User {message.from_user.id} uploaded {file_type}, total files: {len(files)}")


@router.callback_query(F.data == "confirm:send", LeadForm.preview)
async def confirm_send_lead(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработка подтверждения отправки заявки.
    
    Сохраняет заявку в БД и отправляет уведомление админу.
    
    Args:
        callback: Callback от кнопки "Отправить"
        state: FSM контекст
    """
    data = await state.get_data()
    lang = data.get('language', 'en')
    user_id = callback.from_user.id
    
    try:
        files = data.get('files', [])
        files_json = json.dumps(files) if files else None
        
        # Сохраняем заявку в БД
        lead_id = save_lead(
            tg_user_id=user_id,
            full_name=data['full_name'],
            phone=data['phone'],
            description=data['description'],
            db_path=DB_PATH,
            email=data.get('email'),
            files=files_json
        )
        
        logger.info(f"Lead #{lead_id} saved for user {user_id}, files: {len(files)}")
        
        # Отправляем уведомление админу
        await send_admin_notification(
            bot=callback.bot,
            lead_id=lead_id,
            tg_user_id=user_id,
            full_name=data['full_name'],
            phone=data['phone'],
            email=data.get('email'),
            description=data['description'],
            lang=lang,
            files=files
        )
        
        # Очищаем состояние
        await state.clear()
        
        # Отправляем благодарность пользователю с главным меню
        await callback.message.edit_text(get_text('thank_you', lang))
        
        # Показываем главное меню с кнопками управления
        await callback.bot.send_message(
            chat_id=user_id,
            text=get_text('menu', lang),
            reply_markup=get_main_menu_keyboard(lang)
        )
        
        await callback.answer()
        
        logger.info(f"Lead #{lead_id} completed successfully")
        
    except Exception as e:
        logger.error(f"Error saving lead: {e}", exc_info=True)
        await callback.message.edit_text(get_text('error_occurred', lang))
        await callback.answer()
        await state.clear()


@router.callback_query(F.data == "confirm:cancel", LeadForm.preview)
async def confirm_cancel_lead(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработка отмены заявки из preview.
    
    Args:
        callback: Callback от кнопки "Отменить"
        state: FSM контекст
    """
    data = await state.get_data()
    lang = data.get('language', 'en')
    
    # Очищаем состояние
    await state.clear()
    
    await callback.message.edit_text(get_text('cancelled', lang))
    await callback.answer()
    logger.info(f"User {callback.from_user.id} cancelled lead from preview")


@router.callback_query(F.data == "files:cancel", LeadForm.waiting_for_files)
async def cancel_from_files(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработка отмены заявки при загрузке файлов.
    
    Args:
        callback: Callback от кнопки "Отменить"
        state: FSM контекст
    """
    data = await state.get_data()
    lang = data.get('language', 'en')
    
    # Очищаем состояние
    await state.clear()
    
    await callback.message.edit_text(get_text('cancelled', lang))
    await callback.answer()
    logger.info(f"User {callback.from_user.id} cancelled lead from files upload")


@router.callback_query(F.data == "confirm:edit", LeadForm.preview)
async def confirm_edit_lead(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработка запроса на редактирование заявки.
    
    Показывает клавиатуру с выбором поля для редактирования.
    
    Args:
        callback: Callback от кнопки "Изменить"
        state: FSM контекст
    """
    data = await state.get_data()
    lang = data.get('language', 'en')
    
    await state.set_state(LeadForm.editing)
    
    await callback.message.edit_text(
        get_text('choose_field_to_edit', lang),
        reply_markup=get_edit_keyboard(lang)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("edit:"), LeadForm.editing)
async def process_field_selection(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработка выбора поля для редактирования.
    
    Args:
        callback: Callback с выбранным полем (edit:name, edit:phone, etc.)
        state: FSM контекст
    """
    data = await state.get_data()
    lang = data.get('language', 'en')
    
    field = callback.data.split(":")[1]  # name, phone, email, description
    
    # Сохраняем какое поле редактируем
    await state.update_data(editing_field=field)
    
    # Устанавливаем соответствующее состояние
    if field == "name":
        await state.set_state(LeadForm.waiting_for_name)
        await callback.message.edit_text(get_text('ask_name', lang))
    elif field == "phone":
        await state.set_state(LeadForm.waiting_for_phone)
        await callback.message.edit_text(get_text('ask_phone', lang))
    elif field == "email":
        await state.set_state(LeadForm.waiting_for_email)
        await callback.message.edit_text(
            get_text('ask_email', lang),
            reply_markup=get_skip_keyboard(lang)
        )
    elif field == "description":
        await state.set_state(LeadForm.waiting_for_description)
        await callback.message.edit_text(get_text('ask_description', lang))
    
    await callback.answer()
    logger.debug(f"User {callback.from_user.id} editing field: {field}")
