"""
AI Enhancer - улучшение и структурирование описаний проектов.

Этот модуль обрабатывает описания проектов от пользователей и:
- Структурирует информацию
- Извлекает ключевые требования
- Форматирует для читабельности администратора
- (Опционально) Использует AI для улучшения текста
"""
import re
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


def extract_key_points(description: str) -> List[str]:
    """
    Извлекает ключевые пункты из описания.
    
    Разбивает текст на предложения и определяет важные пункты.
    
    Args:
        description: Исходное описание проекта
        
    Returns:
        Список ключевых пунктов
    """
    # Разбиваем на предложения
    sentences = re.split(r'[.!?;]\s+', description)
    
    # Фильтруем пустые и короткие
    key_points = [s.strip() for s in sentences if len(s.strip()) > 5]
    
    return key_points


def detect_project_type(description: str) -> Optional[str]:
    """
    Определяет тип проекта по ключевым словам.
    
    Args:
        description: Описание проекта
        
    Returns:
        Тип проекта или None
    """
    description_lower = description.lower()
    
    # Словарь типов проектов и их ключевых слов
    project_types = {
        'Ремонт': ['ремонт', 'renovation', 'renovacija', 'отделка', 'finishing'],
        'Строительство': ['строительство', 'construction', 'gradnja', 'постройка', 'build'],
        'Сантехника': ['сантехника', 'plumbing', 'водопровод', 'канализация', 'pipes'],
        'Электрика': ['электрика', 'electrical', 'električni', 'проводка', 'wiring'],
        'Кровля': ['крыша', 'кровля', 'roof', 'roofing', 'кров'],
        'Фасад': ['фасад', 'facade', 'fasada', 'внешняя отделка'],
        'Интерьер': ['интерьер', 'interior', 'дизайн', 'design'],
        'Ландшафт': ['ландшафт', 'landscape', 'участок', 'garden', 'yard'],
    }
    
    for project_type, keywords in project_types.items():
        for keyword in keywords:
            if keyword in description_lower:
                return project_type
    
    return None


def extract_urgency(description: str) -> Optional[str]:
    """
    Определяет срочность проекта по ключевым словам.
    
    Args:
        description: Описание проекта
        
    Returns:
        Уровень срочности или None
    """
    description_lower = description.lower()
    
    urgent_keywords = [
        'срочно', 'urgent', 'hitno', 'быстро', 'quickly',
        'asap', 'немедленно', 'сегодня', 'today', 'danas'
    ]
    
    for keyword in urgent_keywords:
        if keyword in description_lower:
            return '🔴 Срочно'
    
    return '⚪ Обычный приоритет'


def extract_budget_mention(description: str) -> Optional[str]:
    """
    Ищет упоминание бюджета в описании.
    
    Args:
        description: Описание проекта
        
    Returns:
        Информация о бюджете если найдена
    """
    # Паттерны для поиска цифр с валютой
    patterns = [
        r'(\d+[\s,]?\d*)\s*€',
        r'(\d+[\s,]?\d*)\s*евро',
        r'(\d+[\s,]?\d*)\s*euro',
        r'бюджет[:\s]+(\d+)',
        r'budget[:\s]+(\d+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, description.lower())
        if match:
            return f"💰 Упомянут бюджет: ~{match.group(1)}"
    
    return None


def structure_description(
    description: str,
    full_name: str,
    phone: str,
    email: Optional[str] = None
) -> Dict[str, any]:
    """
    Структурирует описание проекта и извлекает ключевую информацию.
    
    Args:
        description: Исходное описание
        full_name: Имя клиента
        phone: Телефон клиента
        email: Email клиента (опционально)
        
    Returns:
        Словарь со структурированной информацией
    """
    # Извлекаем ключевые пункты
    key_points = extract_key_points(description)
    
    # Определяем тип проекта
    project_type = detect_project_type(description)
    
    # Определяем срочность
    urgency = extract_urgency(description)
    
    # Ищем бюджет
    budget = extract_budget_mention(description)
    
    structured = {
        'original_description': description,
        'key_points': key_points,
        'project_type': project_type,
        'urgency': urgency,
        'budget': budget,
        'client_name': full_name,
        'client_phone': phone,
        'client_email': email,
        'analysis_timestamp': datetime.now().isoformat()
    }
    
    return structured


def format_enhanced_description(structured: Dict[str, any], lang: str = 'ru') -> str:
    """
    Форматирует улучшенное описание для администратора.
    
    Args:
        structured: Структурированные данные
        lang: Язык форматирования
        
    Returns:
        Отформатированное описание
    """
    lines = []
    
    # Заголовок
    if lang == 'ru':
        lines.append('📋 СТРУКТУРИРОВАННАЯ ЗАЯВКА')
    elif lang == 'me':
        lines.append('📋 STRUKTURIRANA PRIJAVA')
    else:
        lines.append('📋 STRUCTURED REQUEST')
    
    lines.append('')
    
    # Тип проекта
    if structured['project_type']:
        lines.append(f"🏗️ Тип проекта: {structured['project_type']}")
        lines.append('')
    
    # Срочность
    if structured['urgency']:
        lines.append(f"{structured['urgency']}")
        lines.append('')
    
    # Бюджет
    if structured['budget']:
        lines.append(structured['budget'])
        lines.append('')
    
    # Ключевые требования
    if structured['key_points']:
        if lang == 'ru':
            lines.append('✅ Ключевые требования:')
        elif lang == 'me':
            lines.append('✅ Ključni zahtjevi:')
        else:
            lines.append('✅ Key Requirements:')
        
        for i, point in enumerate(structured['key_points'], 1):
            lines.append(f"  {i}. {point}")
        lines.append('')
    
    # Оригинальное описание
    if lang == 'ru':
        lines.append('📝 Оригинальное описание клиента:')
    elif lang == 'me':
        lines.append('📝 Originalni opis klijenta:')
    else:
        lines.append('📝 Original Client Description:')
    
    lines.append(f'"{structured["original_description"]}"')
    
    return '\n'.join(lines)


def enhance_lead_description(
    description: str,
    full_name: str,
    phone: str,
    email: Optional[str] = None,
    lang: str = 'ru',
    use_ai: bool = False
) -> str:
    """
    Главная функция для улучшения описания заявки.
    
    Args:
        description: Исходное описание
        full_name: Имя клиента
        phone: Телефон
        email: Email (опционально)
        lang: Язык
        use_ai: Использовать ли AI (пока не реализовано)
        
    Returns:
        Улучшенное описание для администратора
    """
    try:
        # Структурируем описание
        structured = structure_description(description, full_name, phone, email)
        
        # Форматируем для админа
        enhanced = format_enhanced_description(structured, lang)
        
        logger.info(f"Enhanced description for {full_name}")
        
        return enhanced
        
    except Exception as e:
        logger.error(f"Error enhancing description: {e}", exc_info=True)
        # Fallback - возвращаем оригинальное описание
        return description


# TODO: Интеграция с OpenAI API для продвинутого улучшения
# def enhance_with_ai(description: str, lang: str) -> str:
#     """
#     Использует OpenAI GPT для улучшения описания.
#     Требует OPENAI_API_KEY в .env
#     """
#     pass
