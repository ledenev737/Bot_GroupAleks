"""
Common handlers - общие команды бота (/help, /cancel, /language).

Этот модуль реализует:
- Команду /help для справки
- Команду /cancel для отмены текущей формы
- Команду /language для смены языка
"""
import logging
import asyncio

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext

from app.config import DB_PATH
from app.db import get_user_language, save_user_language
from app.locales import get_text, SUPPORTED_LANGUAGES
from app.keyboards import (
    get_language_keyboard, 
    get_main_menu_keyboard,
    get_language_change_confirmation_keyboard
)

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """
    Обработчик команды /help - показывает справку.
    
    Справка отображается на языке, выбранном пользователем.
    Если язык не установлен, используется английский.
    
    Args:
        message: Сообщение с командой /help
    """
    user_id = message.from_user.id
    user_lang = get_user_language(user_id, DB_PATH) or 'en'
    
    help_text = get_text('help_text', user_lang)
    await message.answer(help_text)
    
    logger.info(f"User {user_id} requested help (lang: {user_lang})")


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    """
    Обработчик команды /cancel - отменяет текущую форму.
    
    Очищает состояние FSM и уведомляет пользователя об отмене.
    Если пользователь не в процессе заполнения формы, команда игнорируется.
    
    Args:
        message: Сообщение с командой /cancel
        state: FSM контекст для очистки состояния
    """
    user_id = message.from_user.id
    user_lang = get_user_language(user_id, DB_PATH) or 'en'
    
    # Проверяем, есть ли активное состояние
    current_state = await state.get_state()
    
    if current_state is None:
        # Пользователь не в процессе заполнения формы
        # Можно либо ничего не делать, либо показать справку
        await message.answer(get_text('menu', user_lang))
        logger.debug(f"User {user_id} used /cancel but no active form")
        return
    
    # Очищаем состояние
    await state.clear()
    
    await message.answer(get_text('cancelled', user_lang))
    logger.info(f"User {user_id} cancelled form (was in state: {current_state})")


@router.message(Command("language"))
async def cmd_language(message: Message, state: FSMContext) -> None:
    """
    Обработчик команды /language - позволяет сменить язык интерфейса.
    
    Если пользователь в процессе заполнения формы, показывает предупреждение.
    Иначе показывает клавиатуру выбора языка.
    
    Args:
        message: Сообщение с командой /language
        state: FSM контекст для проверки состояния
    """
    user_id = message.from_user.id
    user_lang = get_user_language(user_id, DB_PATH) or 'en'
    
    # Проверяем, есть ли активное состояние (пользователь заполняет форму)
    current_state = await state.get_state()
    
    if current_state is not None:
        # Пользователь в процессе заполнения формы - показываем предупреждение
        await message.answer(
            get_text('language_change_warning', user_lang),
            reply_markup=get_language_change_confirmation_keyboard(user_lang)
        )
        logger.info(f"User {user_id} requested language change during form fill (state: {current_state})")
    else:
        # Нет активной формы - показываем выбор языка
        await message.answer(
            get_text('change_language', user_lang),
            reply_markup=get_language_keyboard(callback_prefix="change_lang")
        )
        logger.info(f"User {user_id} requested language change")


@router.message(F.text.in_([
    get_text('btn_change_language', 'ru'),
    get_text('btn_change_language', 'me'),
    get_text('btn_change_language', 'en')
]))
async def btn_language(message: Message, state: FSMContext) -> None:
    """
    Обработчик кнопки "Сменить язык" из главного меню.
    
    Если пользователь в процессе заполнения формы, показывает предупреждение.
    Иначе показывает клавиатуру выбора языка.
    
    Args:
        message: Сообщение с текстом кнопки
        state: FSM контекст для проверки состояния
    """
    user_id = message.from_user.id
    user_lang = get_user_language(user_id, DB_PATH) or 'en'
    
    # Проверяем, есть ли активное состояние (пользователь заполняет форму)
    current_state = await state.get_state()
    
    if current_state is not None:
        # Пользователь в процессе заполнения формы - показываем предупреждение
        await message.answer(
            get_text('language_change_warning', user_lang),
            reply_markup=get_language_change_confirmation_keyboard(user_lang)
        )
        logger.info(f"User {user_id} pressed language change button during form fill (state: {current_state})")
    else:
        # Нет активной формы - показываем выбор языка
        await message.answer(
            get_text('change_language', user_lang),
            reply_markup=get_language_keyboard(callback_prefix="change_lang")
        )
        logger.info(f"User {user_id} pressed language change button")


@router.callback_query(F.data.startswith("confirm_lang_change:"))
async def confirm_language_change_during_form(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик подтверждения/отмены смены языка во время заполнения формы.
    
    Callback data format: confirm_lang_change:yes, confirm_lang_change:no
    
    Args:
        callback: Callback query от кнопки подтверждения
        state: FSM контекст
    """
    try:
        action = callback.data.split(":")[1]
        user_id = callback.from_user.id
        user_lang = get_user_language(user_id, DB_PATH) or 'en'
        
        if action == "yes":
            # Пользователь подтвердил смену языка - очищаем state и показываем выбор языка
            await state.clear()
            
            # Удаляем сообщение с предупреждением
            try:
                await callback.message.delete()
            except:
                pass
            
            # Показываем выбор языка
            await callback.message.answer(
                get_text('change_language', user_lang),
                reply_markup=get_language_keyboard(callback_prefix="change_lang")
            )
            
            logger.info(f"User {user_id} confirmed language change, form data cleared")
        else:
            # Пользователь отменил смену языка - продолжаем заполнение
            await callback.answer(
                "✅" if user_lang == 'en' else "✅",
                show_alert=False
            )
            
            # Удаляем сообщение с предупреждением
            try:
                await callback.message.delete()
            except:
                pass
            
            logger.info(f"User {user_id} cancelled language change, continuing form")
            
    except Exception as e:
        logger.error(f"Error processing language change confirmation: {e}", exc_info=True)
        await callback.answer("An error occurred", show_alert=True)


@router.callback_query(F.data.startswith("change_lang:"))
async def process_language_change(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработчик смены языка через callback.
    
    Сохраняет новый язык пользователя и обновляет сообщение.
    Очищает текущее состояние FSM (если было активно).
    
    Callback data format: change_lang:ru, change_lang:me, change_lang:en
    
    Args:
        callback: Callback query от кнопки выбора языка
        state: FSM контекст (очищается)
    """
    try:
        lang_code = callback.data.split(":")[1]
        
        # Валидация кода языка
        if lang_code not in SUPPORTED_LANGUAGES:
            await callback.answer("Invalid language selection", show_alert=True)
            logger.warning(f"Invalid language code attempted: {lang_code}")
            return
        
        user_id = callback.from_user.id
        old_lang = get_user_language(user_id, DB_PATH)
        save_user_language(user_id, lang_code, DB_PATH)
        
        # Очищаем состояние FSM (форма будет сброшена)
        await state.clear()
        
        # Удаляем inline-сообщение с выбором языка
        try:
            await callback.message.delete()
        except:
            pass  # Игнорируем ошибку если не удалось удалить
        
        await callback.answer(get_text('language_changed', lang_code))
        
        # Отправляем сообщение с удалением старой клавиатуры
        await callback.message.answer(
            get_text('language_changed', lang_code),
            reply_markup=ReplyKeyboardRemove()
        )
        
        # Небольшая задержка чтобы Telegram успел обработать удаление клавиатуры
        await asyncio.sleep(0.3)
        
        # Затем показываем приветствие и меню с новой клавиатурой
        welcome_text = get_text('welcome', lang_code)
        menu_text = get_text('menu', lang_code)
        await callback.message.answer(
            f"{welcome_text}\n\n{menu_text}",
            reply_markup=get_main_menu_keyboard(lang_code)
        )
        
        logger.info(f"User {user_id} changed language from {old_lang} to {lang_code}")
        
    except Exception as e:
        logger.error(f"Error processing language change: {e}", exc_info=True)
        await callback.answer("An error occurred", show_alert=True)
