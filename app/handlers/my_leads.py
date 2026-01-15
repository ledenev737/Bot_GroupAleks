"""
My Leads handlers - просмотр и управление заявками пользователя.

Этот модуль реализует:
- Команду /my_leads для просмотра заявок
- Отмену заявок с подтверждением
- Обработку кнопок главного меню
"""
import logging
from datetime import datetime

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.config import DB_PATH
from app.db import get_user_language, get_user_leads, delete_lead
from app.locales import get_text, format_text
from app.keyboards import (
    get_main_menu_keyboard,
    get_leads_list_keyboard,
    get_confirm_cancel_keyboard
)

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.text.in_([
    '➕ Новая заявка', '➕ Novi zahtjev', '➕ New request'
]))
async def btn_new_lead(message: Message, state: FSMContext) -> None:
    """
    Обработка кнопки "Новая заявка" из главного меню.
    
    Перенаправляет на команду /new
    """
    # Импортируем здесь чтобы избежать циклического импорта
    from app.handlers.lead_flow import cmd_new_lead
    await cmd_new_lead(message, state)


@router.message(F.text.in_([
    '📋 Мои заявки', '📋 Moji zahtjevi', '📋 My requests'
]))
@router.message(Command("my_leads"))
async def cmd_my_leads(message: Message) -> None:
    """
    Показать список всех заявок пользователя.
    
    Args:
        message: Сообщение с командой /my_leads или кнопкой
    """
    user_id = message.from_user.id
    user_lang = get_user_language(user_id, DB_PATH) or 'en'
    
    # Получаем заявки пользователя
    leads = get_user_leads(user_id, DB_PATH)
    
    if not leads:
        await message.answer(
            get_text('no_leads', user_lang),
            reply_markup=get_main_menu_keyboard(user_lang)
        )
        logger.info(f"User {user_id} has no leads")
        return
    
    # Формируем список заявок
    leads_text = get_text('my_leads', user_lang)
    
    for lead in leads:
        # Форматируем дату
        created_date = lead['created_at'].split('T')[0]  # YYYY-MM-DD
        
        # Короткое описание
        short_desc = lead['description'][:50] + '...' if len(lead['description']) > 50 else lead['description']
        
        leads_text += (
            f"📋 <b>Заявка #{lead['id']}</b>\n"
            f"📝 {short_desc}\n"
            f"📅 {created_date}\n"
            f"───────────────\n\n"
        )
    
    await message.answer(
        leads_text,
        reply_markup=get_main_menu_keyboard(user_lang),
        parse_mode='HTML'
    )
    logger.info(f"User {user_id} viewed {len(leads)} leads")


@router.message(F.text.in_([
    '❌ Отменить заявку', '❌ Otkazati zahtjev', '❌ Cancel request'
]))
async def btn_cancel_lead(message: Message, state: FSMContext) -> None:
    """
    Обработка кнопки "Отменить заявку" из главного меню.
    
    Показывает список заявок для выбора.
    """
    user_id = message.from_user.id
    user_lang = get_user_language(user_id, DB_PATH) or 'en'
    
    # Получаем заявки пользователя
    leads = get_user_leads(user_id, DB_PATH)
    
    if not leads:
        await message.answer(
            get_text('no_leads', user_lang),
            reply_markup=get_main_menu_keyboard(user_lang)
        )
        return
    
    # Показываем список заявок для выбора
    await message.answer(
        get_text('choose_lead_to_cancel', user_lang),
        reply_markup=get_leads_list_keyboard(leads, user_lang)
    )
    logger.info(f"User {user_id} wants to cancel a lead, showing {len(leads)} options")


@router.callback_query(F.data.startswith("select_lead:"))
async def process_lead_selection(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Обработка выбора заявки для отмены.
    
    Показывает подтверждение с деталями заявки.
    """
    user_id = callback.from_user.id
    user_lang = get_user_language(user_id, DB_PATH) or 'en'
    
    # Получаем ID заявки
    lead_id = int(callback.data.split(":")[1])
    
    # Получаем заявки пользователя
    leads = get_user_leads(user_id, DB_PATH)
    lead = next((l for l in leads if l['id'] == lead_id), None)
    
    if not lead:
        await callback.answer(get_text('cancel_failed', user_lang), show_alert=True)
        return
    
    # Форматируем дату
    created_date = lead['created_at'].split('T')[0]
    
    # Короткое описание для подтверждения
    short_desc = lead['description'][:100] + '...' if len(lead['description']) > 100 else lead['description']
    
    confirm_text = format_text(
        'confirm_cancel_lead',
        user_lang,
        lead_id=lead_id,
        description=short_desc,
        created_at=created_date
    )
    
    # Сохраняем ID заявки в state для подтверждения
    await state.update_data(cancel_lead_id=lead_id)
    
    await callback.message.edit_text(
        confirm_text,
        reply_markup=get_confirm_cancel_keyboard(user_lang)
    )
    await callback.answer()
    logger.info(f"User {user_id} selected lead #{lead_id} for cancellation")


@router.callback_query(F.data == "cancel_lead:confirm")
async def confirm_cancel_lead(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Подтверждение отмены заявки - удаление из БД.
    """
    user_id = callback.from_user.id
    user_lang = get_user_language(user_id, DB_PATH) or 'en'
    
    # Получаем ID заявки из state
    data = await state.get_data()
    lead_id = data.get('cancel_lead_id')
    
    if not lead_id:
        await callback.answer(get_text('cancel_failed', user_lang), show_alert=True)
        return
    
    # Удаляем заявку из БД
    success = delete_lead(lead_id, user_id, DB_PATH)
    
    if success:
        success_text = format_text('lead_cancelled', user_lang, lead_id=lead_id)
        await callback.message.edit_text(success_text)
        logger.info(f"User {user_id} cancelled and deleted lead #{lead_id}")
        
        # Показываем главное меню
        await callback.message.answer(
            get_text('menu', user_lang),
            reply_markup=get_main_menu_keyboard(user_lang)
        )
    else:
        await callback.answer(get_text('cancel_failed', user_lang), show_alert=True)
        logger.warning(f"Failed to delete lead #{lead_id} for user {user_id}")
    
    # Очищаем state
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "cancel_lead:back")
async def back_from_confirm(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Возврат из подтверждения отмены к списку заявок.
    """
    user_id = callback.from_user.id
    user_lang = get_user_language(user_id, DB_PATH) or 'en'
    
    # Получаем заявки снова
    leads = get_user_leads(user_id, DB_PATH)
    
    if not leads:
        await callback.message.edit_text(get_text('no_leads', user_lang))
        await callback.answer()
        return
    
    # Показываем список заявок
    await callback.message.edit_text(
        get_text('choose_lead_to_cancel', user_lang),
        reply_markup=get_leads_list_keyboard(leads, user_lang)
    )
    
    # Очищаем state
    await state.clear()
    await callback.answer()


@router.callback_query(F.data == "leads:back")
async def back_to_menu(callback: CallbackQuery) -> None:
    """
    Возврат из списка заявок к главному меню.
    """
    user_id = callback.from_user.id
    user_lang = get_user_language(user_id, DB_PATH) or 'en'
    
    await callback.message.edit_text(get_text('menu', user_lang))
    await callback.answer()
