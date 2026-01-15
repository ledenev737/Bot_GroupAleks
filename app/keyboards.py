"""
Модуль для создания клавиатур (inline кнопок и reply кнопок)
"""
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from app.locales import get_text, LANGUAGE_NAMES


def get_language_keyboard(callback_prefix: str = "lang") -> InlineKeyboardMarkup:
    """
    Клавиатура для выбора языка (RU / ME / EN)
    
    Args:
        callback_prefix: Префикс для callback_data (по умолчанию "lang")
                        Может быть "lang" для первого выбора или "change_lang" для смены
    
    Returns:
        InlineKeyboardMarkup с кнопками выбора языка
    """
    builder = InlineKeyboardBuilder()
    
    # Добавляем кнопки для каждого языка
    for lang_code, lang_name in LANGUAGE_NAMES.items():
        builder.button(
            text=lang_name,
            callback_data=f"{callback_prefix}:{lang_code}"
        )
    
    # Размещаем кнопки в один столбец (по одной в ряд)
    builder.adjust(1)
    
    return builder.as_markup()


def get_confirmation_keyboard(lang: str = 'en') -> InlineKeyboardMarkup:
    """
    Клавиатура для подтверждения отправки заявки (Отправить / Изменить / Отменить)
    
    Args:
        lang: Код языка для локализации кнопок
        
    Returns:
        InlineKeyboardMarkup с кнопками подтверждения
    """
    builder = InlineKeyboardBuilder()
    
    # Кнопка "Отправить"
    builder.button(
        text=get_text('btn_send', lang),
        callback_data="confirm:send"
    )
    
    # Кнопка "Изменить"
    builder.button(
        text=get_text('btn_edit', lang),
        callback_data="confirm:edit"
    )
    
    # Кнопка "Отменить"
    builder.button(
        text=get_text('btn_cancel', lang),
        callback_data="confirm:cancel"
    )
    
    # Размещаем кнопки: первые две в ряд, отмена отдельно
    builder.adjust(2, 1)
    
    return builder.as_markup()


def get_edit_keyboard(lang: str = 'en') -> InlineKeyboardMarkup:
    """
    Клавиатура для выбора поля для редактирования
    (Имя / Телефон / Email / Описание)
    
    Args:
        lang: Код языка для локализации кнопок
        
    Returns:
        InlineKeyboardMarkup с кнопками выбора поля
    """
    builder = InlineKeyboardBuilder()
    
    # Кнопка "Имя"
    builder.button(
        text=get_text('btn_name', lang),
        callback_data="edit:name"
    )
    
    # Кнопка "Телефон"
    builder.button(
        text=get_text('btn_phone', lang),
        callback_data="edit:phone"
    )
    
    # Кнопка "Email"
    builder.button(
        text=get_text('btn_email', lang),
        callback_data="edit:email"
    )
    
    # Кнопка "Описание"
    builder.button(
        text=get_text('btn_description', lang),
        callback_data="edit:description"
    )
    
    # Размещаем кнопки по 2 в ряд
    builder.adjust(2)
    
    return builder.as_markup()


def get_skip_keyboard(lang: str = 'en') -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой "Пропустить" (для email)
    
    Args:
        lang: Код языка для локализации кнопки
        
    Returns:
        InlineKeyboardMarkup с кнопкой "Пропустить"
    """
    builder = InlineKeyboardBuilder()
    
    # Кнопка "Пропустить"
    builder.button(
        text=get_text('btn_skip', lang),
        callback_data="skip:email"
    )
    
    return builder.as_markup()


def remove_keyboard() -> InlineKeyboardMarkup:
    """
    Пустая клавиатура (для удаления кнопок)
    
    Returns:
        Пустая InlineKeyboardMarkup
    """
    return InlineKeyboardMarkup(inline_keyboard=[])


def get_confirm_data_keyboard(lang: str = 'en') -> InlineKeyboardMarkup:
    """
    Клавиатура для подтверждения использования старых данных
    (Использовать / Изменить)
    
    Args:
        lang: Код языка для локализации кнопок
        
    Returns:
        InlineKeyboardMarkup с кнопками подтверждения
    """
    builder = InlineKeyboardBuilder()
    
    # Кнопка "Использовать эти данные"
    builder.button(
        text=get_text('btn_use_data', lang),
        callback_data="confirm_data:use"
    )
    
    # Кнопка "Изменить данные"
    builder.button(
        text=get_text('btn_change_data', lang),
        callback_data="confirm_data:change"
    )
    
    # Размещаем кнопки в один столбец
    builder.adjust(1)
    
    return builder.as_markup()


def get_main_menu_keyboard(lang: str = 'en') -> ReplyKeyboardMarkup:
    """
    Главное меню с постоянными кнопками внизу
    (Новая заявка / Мои заявки / Отменить заявку / Сменить язык)
    
    Args:
        lang: Код языка для локализации кнопок
        
    Returns:
        ReplyKeyboardMarkup с постоянными кнопками
    """
    builder = ReplyKeyboardBuilder()
    
    # Первый ряд
    builder.button(text=get_text('btn_new_lead', lang))
    builder.button(text=get_text('btn_my_leads', lang))
    
    # Второй ряд
    builder.button(text=get_text('btn_cancel_lead', lang))
    builder.button(text=get_text('btn_change_language', lang))
    
    # Настройка расположения: 2 кнопки в первом ряду, 2 во втором
    builder.adjust(2, 2)
    
    return builder.as_markup(resize_keyboard=True)


def get_leads_list_keyboard(leads: list, lang: str = 'en') -> InlineKeyboardMarkup:
    """
    Клавиатура со списком заявок для отмены
    
    Args:
        leads: Список заявок пользователя
        lang: Код языка
        
    Returns:
        InlineKeyboardMarkup с кнопками заявок
    """
    builder = InlineKeyboardBuilder()
    
    for lead in leads:
        # Короткое описание для кнопки (первые 30 символов)
        short_desc = lead['description'][:30] + '...' if len(lead['description']) > 30 else lead['description']
        button_text = f"#{lead['id']} - {short_desc}"
        
        builder.button(
            text=button_text,
            callback_data=f"select_lead:{lead['id']}"
        )
    
    # Кнопка "Назад"
    builder.button(
        text=get_text('btn_back', lang),
        callback_data="leads:back"
    )
    
    # Размещаем по 1 заявке в ряд
    builder.adjust(1)
    
    return builder.as_markup()


def get_confirm_cancel_keyboard(lang: str = 'en') -> InlineKeyboardMarkup:
    """
    Клавиатура подтверждения отмены заявки
    (Да, отменить / Назад)
    
    Args:
        lang: Код языка
        
    Returns:
        InlineKeyboardMarkup с кнопками подтверждения
    """
    builder = InlineKeyboardBuilder()
    
    # Кнопка "Да, отменить"
    builder.button(
        text=get_text('btn_confirm', lang),
        callback_data="cancel_lead:confirm"
    )
    
    # Кнопка "Назад"
    builder.button(
        text=get_text('btn_back', lang),
        callback_data="cancel_lead:back"
    )
    
    # Размещаем в один столбец
    builder.adjust(1)
    
    return builder.as_markup()


def get_files_keyboard(lang: str = 'en') -> InlineKeyboardMarkup:
    """
    Клавиатура для завершения загрузки файлов
    (Готово / Пропустить / Отменить)
    
    Args:
        lang: Код языка для локализации кнопок
        
    Returns:
        InlineKeyboardMarkup с кнопками
    """
    builder = InlineKeyboardBuilder()
    
    # Кнопка "Готово"
    builder.button(
        text=get_text('btn_done', lang),
        callback_data="files:done"
    )
    
    # Кнопка "Пропустить"
    builder.button(
        text=get_text('btn_skip', lang),
        callback_data="files:skip"
    )
    
    # Кнопка "Отменить"
    builder.button(
        text=get_text('btn_cancel', lang),
        callback_data="files:cancel"
    )
    
    # Размещаем кнопки: первые две в ряд, отмена отдельно
    builder.adjust(2, 1)
    
    return builder.as_markup()


def get_language_change_confirmation_keyboard(lang: str = 'en') -> InlineKeyboardMarkup:
    """
    Клавиатура подтверждения смены языка во время заполнения формы
    (Да, сменить язык / Нет, продолжить заполнение)
    
    Args:
        lang: Код языка для локализации кнопок
        
    Returns:
        InlineKeyboardMarkup с кнопками подтверждения
    """
    builder = InlineKeyboardBuilder()
    
    # Кнопка "Да, сменить язык"
    builder.button(
        text=get_text('btn_confirm_language_change', lang),
        callback_data="confirm_lang_change:yes"
    )
    
    # Кнопка "Нет, продолжить заполнение"
    builder.button(
        text=get_text('btn_continue_form', lang),
        callback_data="confirm_lang_change:no"
    )
    
    # Размещаем кнопки в один столбец
    builder.adjust(1)
    
    return builder.as_markup()