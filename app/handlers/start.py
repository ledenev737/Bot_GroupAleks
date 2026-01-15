"""
Start command and language selection handlers.

This module handles:
- /start command (initial greeting or language selection)
- Language selection via inline buttons
"""
from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
import logging

from app.config import DB_PATH
from app.db import get_user_language, save_user_language
from app.locales import get_text, SUPPORTED_LANGUAGES
from app.keyboards import get_language_keyboard, get_main_menu_keyboard

router = Router()
logger = logging.getLogger(__name__)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext = None) -> None:
    """
    Handle /start command.
    
    Flow:
    - If user language is set: show welcome message and menu
    - If not set: show language selection buttons
    - If user is in FSM state: clear it first
    
    Args:
        message: Incoming message with /start command
        state: FSM context (optional, for clearing state)
    """
    user_id = message.from_user.id
    user_lang = get_user_language(user_id, DB_PATH)
    
    # Если пользователь в процессе заполнения формы - очищаем состояние
    if state:
        current_state = await state.get_state()
        if current_state:
            await state.clear()
            logger.info(f"User {user_id} used /start, cleared state: {current_state}")
    
    if user_lang:
        welcome_text = get_text('welcome', user_lang)
        menu_text = get_text('menu', user_lang)
        await message.answer(
            f"{welcome_text}\n\n{menu_text}",
            reply_markup=get_main_menu_keyboard(user_lang)
        )
        logger.info(f"User {user_id} accessed /start with language {user_lang}")
    else:
        await message.answer(
            get_text('choose_language', 'en'),
            reply_markup=get_language_keyboard()
        )
        logger.info(f"New user {user_id} requested language selection")


@router.callback_query(F.data.startswith("lang:"))
async def process_language_selection(callback: CallbackQuery) -> None:
    """
    Handle language selection callback.
    
    Callback data format: lang:ru, lang:me, lang:en
    
    Args:
        callback: Callback query from language selection button
    """
    try:
        lang_code = callback.data.split(":")[1]
        
        # Validate language code
        if lang_code not in SUPPORTED_LANGUAGES:
            await callback.answer("Invalid language selection", show_alert=True)
            logger.warning(f"Invalid language code attempted: {lang_code}")
            return
        
        user_id = callback.from_user.id
        save_user_language(user_id, lang_code, DB_PATH)
        
        welcome_text = get_text('welcome', lang_code)
        menu_text = get_text('menu', lang_code)
        
        # Редактируем сообщение с выбором языка
        await callback.message.edit_text(f"{welcome_text}\n\n{menu_text}")
        
        # Отправляем новое сообщение с reply keyboard (главное меню)
        await callback.message.answer(
            get_text('menu', lang_code),
            reply_markup=get_main_menu_keyboard(lang_code)
        )
        await callback.answer()
        
        logger.info(f"User {user_id} selected language: {lang_code}")
        
    except Exception as e:
        logger.error(f"Error processing language selection: {e}", exc_info=True)
        await callback.answer("An error occurred", show_alert=True)
