"""
FSM States для формы заявки.

Определяет состояния (states) для пошагового сбора информации о заявке.
"""
from aiogram.fsm.state import State, StatesGroup


class LeadForm(StatesGroup):
    """
    Состояния формы заявки.
    
    Последовательность:
    1. confirm_data - подтверждение использования старых данных (для повторных заявок)
    2. waiting_for_name - ожидание имени
    3. waiting_for_phone - ожидание телефона
    4. waiting_for_email - ожидание email (можно пропустить)
    5. waiting_for_description - ожидание описания проекта
    6. waiting_for_files - ожидание файлов (можно пропустить)
    7. preview - просмотр заявки перед отправкой
    8. editing - редактирование конкретного поля
    """
    confirm_data = State()
    waiting_for_name = State()
    waiting_for_phone = State()
    waiting_for_email = State()
    waiting_for_description = State()
    waiting_for_files = State()
    preview = State()
    editing = State()
