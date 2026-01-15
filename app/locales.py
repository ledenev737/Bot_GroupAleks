"""
Локализация - тексты на 3 языках (RU, ME, EN)
"""

# Словарь переводов
TEXTS = {
    # Выбор языка
    'choose_language': {
        'ru': '🌍 Выберите язык / Izaberite jezik / Choose language:',
        'me': '🌍 Izaberite jezik / Выберите язык / Choose language:',
        'en': '🌍 Choose language / Выберите язык / Izaberite jezik:',
    },
    
    # Приветствие
    'welcome': {
        'ru': '👋 Добро пожаловать!\n\n'
              'Я помогу вам оставить заявку на строительно-ремонтные работы.\n\n'
              'Используйте /new для создания новой заявки.',
        'me': '👋 Dobrodošli!\n\n'
              'Pomoći ću vam da pošaljete zahtjev za građevinske i renovacijske radove.\n\n'
              'Koristite /new da kreirate novi zahtjev.',
        'en': '👋 Welcome!\n\n'
              'I will help you submit a request for construction and renovation work.\n\n'
              'Use /new to create a new request.',
    },
    
    # Меню команд
    'menu': {
        'ru': '📋 Доступные команды:\n\n'
              '/new - Создать новую заявку\n'
              '/language - Сменить язык\n'
              '/cancel - Отменить текущую заявку\n'
              '/help - Помощь',
        'me': '📋 Dostupne komande:\n\n'
              '/new - Kreirati novi zahtjev\n'
              '/language - Promijeniti jezik\n'
              '/cancel - Otkazati trenutni zahtjev\n'
              '/help - Pomoć',
        'en': '📋 Available commands:\n\n'
              '/new - Create a new request\n'
              '/language - Change language\n'
              '/cancel - Cancel current request\n'
              '/help - Help',
    },
    
    # Начало заполнения заявки
    'start_new_lead': {
        'ru': '📝 Начинаем заполнение заявки.\n\n'
              'Пожалуйста, укажите ваше имя и фамилию:',
        'me': '📝 Počinjemo popunjavanje zahtjeva.\n\n'
              'Molimo vas da unesete vaše ime i prezime:',
        'en': '📝 Starting a new request.\n\n'
              'Please enter your first and last name:',
    },
    
    # Запрос имени
    'ask_name': {
        'ru': '👤 Введите ваше имя и фамилию:',
        'me': '👤 Unesite vaše ime i prezime:',
        'en': '👤 Enter your first and last name:',
    },
    
    # Запрос телефона
    'ask_phone': {
        'ru': '📞 Введите ваш номер телефона:\n\n'
              'Формат: +382 XX XXX XXX или любой другой удобный формат.',
        'me': '📞 Unesite vaš broj telefona:\n\n'
              'Format: +382 XX XXX XXX ili bilo koji drugi format.',
        'en': '📞 Enter your phone number:\n\n'
              'Format: +382 XX XXX XXX or any other convenient format.',
    },
    
    # Запрос email
    'ask_email': {
        'ru': '✉️ Введите ваш email (или нажмите "Пропустить"):',
        'me': '✉️ Unesite vaš email (ili pritisnite "Preskočiti"):',
        'en': '✉️ Enter your email (or press "Skip"):',
    },
    
    # Запрос описания
    'ask_description': {
        'ru': '📝 Опишите ваш проект:\n\n'
              'Расскажите, какие работы вам нужны (минимум 10 символов).',
        'me': '📝 Opišite vaš projekat:\n\n'
              'Recite nam kakvi radovi su vam potrebni (minimum 10 znakova).',
        'en': '📝 Describe your project:\n\n'
              'Tell us what work you need (minimum 10 characters).',
    },
    
    # Запрос файлов
    'ask_files': {
        'ru': '📎 Прикрепите фото или документы (опционально):\n\n'
              'Вы можете отправить фото, документы или видео.\n'
              'Когда закончите, нажмите "Готово" или "Пропустить".',
        'me': '📎 Priložite fotografije ili dokumente (opciono):\n\n'
              'Možete poslati fotografije, dokumente ili video.\n'
              'Kada završite, pritisnite "Gotovo" ili "Preskočiti".',
        'en': '📎 Attach photos or documents (optional):\n\n'
              'You can send photos, documents or videos.\n'
              'When done, press "Done" or "Skip".',
    },
    
    # Подтверждение старых данных
    'confirm_old_data': {
        'ru': '👤 У вас уже есть заявка.\n\n'
              'Использовать эти данные?\n\n'
              '📋 Имя: {full_name}\n'
              '📞 Телефон: {phone}\n'
              '✉️ Email: {email}',
        'me': '👤 Već imate prijavu.\n\n'
              'Koristiti ove podatke?\n\n'
              '📋 Ime: {full_name}\n'
              '📞 Telefon: {phone}\n'
              '✉️ Email: {email}',
        'en': '👤 You already have an application.\n\n'
              'Use this data?\n\n'
              '📋 Name: {full_name}\n'
              '📞 Phone: {phone}\n'
              '✉️ Email: {email}',
    },
    
    # Файл получен
    'file_received': {
        'ru': '✅ Файл получен! Можете отправить еще или нажмите "Готово".',
        'me': '✅ Fajl primljen! Možete poslati još ili pritisnite "Gotovo".',
        'en': '✅ File received! You can send more or press "Done".',
    },
    
    # Ошибка валидации телефона
    'invalid_phone': {
        'ru': '❌ Неверный формат телефона.\n\n'
              'Пожалуйста, введите номер телефона (минимум 10 цифр).\n'
              'Например: +382 67 123 456',
        'me': '❌ Pogrešan format broja telefona.\n\n'
              'Molimo unesite broj telefona (minimum 10 cifara).\n'
              'Na primjer: +382 67 123 456',
        'en': '❌ Invalid phone format.\n\n'
              'Please enter a phone number (minimum 10 digits).\n'
              'Example: +382 67 123 456',
    },
    
    # Ошибка валидации email
    'invalid_email': {
        'ru': '❌ Неверный формат email.\n\n'
              'Пожалуйста, введите корректный email или нажмите "Пропустить".',
        'me': '❌ Pogrešan format email-a.\n\n'
              'Molimo unesite ispravan email ili pritisnite "Preskočiti".',
        'en': '❌ Invalid email format.\n\n'
              'Please enter a valid email or press "Skip".',
    },
    
    # Ошибка валидации описания
    'description_too_short': {
        'ru': '❌ Описание слишком короткое.\n\n'
              'Пожалуйста, опишите ваш проект подробнее (минимум 10 символов).',
        'me': '❌ Opis je prekratak.\n\n'
              'Molimo opišite vaš projekat detaljnije (minimum 10 znakova).',
        'en': '❌ Description is too short.\n\n'
              'Please describe your project in more detail (minimum 10 characters).',
    },
    
    # Preview заявки перед отправкой
    'preview_lead': {
        'ru': '✅ Проверьте данные перед отправкой:\n\n'
              '👤 Имя: {full_name}\n'
              '📞 Телефон: {phone}\n'
              '✉️ Email: {email}\n'
              '📝 Описание проекта:\n{description}\n\n'
              'Всё верно?',
        'me': '✅ Provjerite podatke prije slanja:\n\n'
              '👤 Ime: {full_name}\n'
              '📞 Telefon: {phone}\n'
              '✉️ Email: {email}\n'
              '📝 Opis projekta:\n{description}\n\n'
              'Da li je sve tačno?',
        'en': '✅ Review your information before submitting:\n\n'
              '👤 Name: {full_name}\n'
              '📞 Phone: {phone}\n'
              '✉️ Email: {email}\n'
              '📝 Project description:\n{description}\n\n'
              'Is everything correct?',
    },
    
    # Email не указан
    'email_not_provided': {
        'ru': 'не указан',
        'me': 'nije navedeno',
        'en': 'not provided',
    },
    
    # Спасибо за заявку
    'thank_you': {
        'ru': '🎉 Спасибо! Ваша заявка принята.\n\n'
              'Мы свяжемся с вами в ближайшее время.\n\n'
              'Используйте кнопки ниже для управления заявками.',
        'me': '🎉 Hvala! Vaš zahtjev je primljen.\n\n'
              'Kontaktiraćemo vas uskoro.\n\n'
              'Koristite dugmad ispod za upravljanje zahtjevima.',
        'en': '🎉 Thank you! Your request has been received.\n\n'
              'We will contact you shortly.\n\n'
              'Use buttons below to manage your requests.',
    },
    
    # Мои заявки
    'my_leads': {
        'ru': '📋 Ваши заявки:\n\n',
        'me': '📋 Vaši zahtjevi:\n\n',
        'en': '📋 Your requests:\n\n',
    },
    
    # Нет заявок
    'no_leads': {
        'ru': '📋 У вас пока нет заявок.\n\n'
              'Используйте /new чтобы создать первую заявку.',
        'me': '📋 Još nemate zahtjeva.\n\n'
              'Koristite /new da kreirate prvi zahtjev.',
        'en': '📋 You have no requests yet.\n\n'
              'Use /new to create your first request.',
    },
    
    # Выбор заявки для отмены
    'choose_lead_to_cancel': {
        'ru': '❌ Выберите заявку для отмены:',
        'me': '❌ Izaberite zahtjev za otkazivanje:',
        'en': '❌ Choose a request to cancel:',
    },
    
    # Подтверждение отмены
    'confirm_cancel_lead': {
        'ru': '⚠️ Вы уверены что хотите отменить эту заявку?\n\n'
              '📋 Заявка #{lead_id}\n'
              '📝 {description}\n'
              '📅 {created_at}\n\n'
              'Эта заявка будет удалена из базы данных.',
        'me': '⚠️ Da li ste sigurni da želite otkazati ovaj zahtjev?\n\n'
              '📋 Zahtjev #{lead_id}\n'
              '📝 {description}\n'
              '📅 {created_at}\n\n'
              'Ovaj zahtjev će biti obrisan iz baze podataka.',
        'en': '⚠️ Are you sure you want to cancel this request?\n\n'
              '📋 Request #{lead_id}\n'
              '📝 {description}\n'
              '📅 {created_at}\n\n'
              'This request will be deleted from the database.',
    },
    
    # Заявка отменена
    'lead_cancelled': {
        'ru': '✅ Заявка #{lead_id} успешно отменена и удалена из базы данных.',
        'me': '✅ Zahtjev #{lead_id} je uspješno otkazan i obrisan iz baze podataka.',
        'en': '✅ Request #{lead_id} has been successfully cancelled and deleted from the database.',
    },
    
    # Не удалось отменить
    'cancel_failed': {
        'ru': '❌ Не удалось отменить заявку. Возможно она уже была удалена.',
        'me': '❌ Nije moguće otkazati zahtjev. Možda je već obrisan.',
        'en': '❌ Failed to cancel request. It may have already been deleted.',
    },
    
    # Отмена заявки
    'cancelled': {
        'ru': '❌ Заявка отменена.\n\n'
              'Используйте /new для создания новой заявки.',
        'me': '❌ Zahtjev je otkazan.\n\n'
              'Koristite /new da kreirate novi zahtjev.',
        'en': '❌ Request cancelled.\n\n'
              'Use /new to create a new request.',
    },
    
    # Выбор поля для редактирования
    'choose_field_to_edit': {
        'ru': '✏️ Выберите поле для редактирования:',
        'me': '✏️ Izaberite polje za izmjenu:',
        'en': '✏️ Choose a field to edit:',
    },
    
    # Команда /help
    'help_text': {
        'ru': '❓ Помощь\n\n'
              '📋 Доступные команды:\n\n'
              '/start - Начало работы\n'
              '/new - Создать новую заявку\n'
              '/language - Сменить язык\n'
              '/cancel - Отменить текущую заявку\n'
              '/help - Показать эту справку\n\n'
              '💡 Как это работает:\n'
              '1. Нажмите /new\n'
              '2. Заполните форму (имя, телефон, email, описание)\n'
              '3. Проверьте данные и отправьте\n'
              '4. Мы получим вашу заявку и свяжемся с вами',
        'me': '❓ Pomoć\n\n'
              '📋 Dostupne komande:\n\n'
              '/start - Početak rada\n'
              '/new - Kreirati novi zahtjev\n'
              '/language - Promijeniti jezik\n'
              '/cancel - Otkazati trenutni zahtjev\n'
              '/help - Prikazati ovu pomoć\n\n'
              '💡 Kako to radi:\n'
              '1. Pritisnite /new\n'
              '2. Popunite formular (ime, telefon, email, opis)\n'
              '3. Provjerite podatke i pošaljite\n'
              '4. Primićemo vaš zahtjev i kontaktiraćemo vas',
        'en': '❓ Help\n\n'
              '📋 Available commands:\n\n'
              '/start - Start\n'
              '/new - Create a new request\n'
              '/language - Change language\n'
              '/cancel - Cancel current request\n'
              '/help - Show this help\n\n'
              '💡 How it works:\n'
              '1. Press /new\n'
              '2. Fill out the form (name, phone, email, description)\n'
              '3. Review and submit\n'
              '4. We will receive your request and contact you',
    },
    
    # Ошибка
    'error_occurred': {
        'ru': '❌ Произошла ошибка. Попробуйте снова или обратитесь в поддержку.',
        'me': '❌ Došlo je do greške. Pokušajte ponovo ili kontaktirajte podršku.',
        'en': '❌ An error occurred. Please try again or contact support.',
    },
    
    # Кнопки
    'btn_send': {
        'ru': '✅ Отправить',
        'me': '✅ Poslati',
        'en': '✅ Send',
    },
    'btn_edit': {
        'ru': '✏️ Изменить',
        'me': '✏️ Izmjeniti',
        'en': '✏️ Edit',
    },
    'btn_skip': {
        'ru': '⏭️ Пропустить',
        'me': '⏭️ Preskočiti',
        'en': '⏭️ Skip',
    },
    'btn_cancel': {
        'ru': '❌ Отменить',
        'me': '❌ Otkazati',
        'en': '❌ Cancel',
    },
    'btn_name': {
        'ru': '👤 Имя',
        'me': '👤 Ime',
        'en': '👤 Name',
    },
    'btn_phone': {
        'ru': '📞 Телефон',
        'me': '📞 Telefon',
        'en': '📞 Phone',
    },
    'btn_email': {
        'ru': '✉️ Email',
        'me': '✉️ Email',
        'en': '✉️ Email',
    },
    'btn_description': {
        'ru': '📝 Описание',
        'me': '📝 Opis',
        'en': '📝 Description',
    },
    'btn_use_data': {
        'ru': '✅ Использовать эти данные',
        'me': '✅ Koristiti ove podatke',
        'en': '✅ Use this data',
    },
    'btn_change_data': {
        'ru': '✏️ Изменить данные',
        'me': '✏️ Promijeniti podatke',
        'en': '✏️ Change data',
    },
    'btn_done': {
        'ru': '✅ Готово',
        'me': '✅ Gotovo',
        'en': '✅ Done',
    },
    'btn_files': {
        'ru': '📎 Файлы',
        'me': '📎 Fajlovi',
        'en': '📎 Files',
    },
    'btn_new_lead': {
        'ru': '➕ Новая заявка',
        'me': '➕ Novi zahtjev',
        'en': '➕ New request',
    },
    'btn_my_leads': {
        'ru': '📋 Мои заявки',
        'me': '📋 Moji zahtjevi',
        'en': '📋 My requests',
    },
    'btn_cancel_lead': {
        'ru': '❌ Отменить заявку',
        'me': '❌ Otkazati zahtjev',
        'en': '❌ Cancel request',
    },
    'btn_back': {
        'ru': '◀️ Назад',
        'me': '◀️ Nazad',
        'en': '◀️ Back',
    },
    'btn_confirm': {
        'ru': '✅ Да, отменить',
        'me': '✅ Da, otkazati',
        'en': '✅ Yes, cancel',
    },
    
    # Уведомление админу
    'admin_notification': {
        'ru': '🧱 Новая заявка',
        'me': '🧱 Novi zahtjev',
        'en': '🧱 New Request',
    },
    
    # Смена языка
    'change_language': {
        'ru': '🌍 Выберите новый язык:',
        'me': '🌍 Izaberite novi jezik:',
        'en': '🌍 Choose a new language:',
    },
    
    'language_changed': {
        'ru': '✅ Язык успешно изменен!',
        'me': '✅ Jezik je uspješno promijenjen!',
        'en': '✅ Language successfully changed!',
    },
    
    'btn_change_language': {
        'ru': '🌍 Сменить язык',
        'me': '🌍 Promijeniti jezik',
        'en': '🌍 Change language',
    },
    
    # Предупреждение о смене языка во время заполнения формы
    'language_change_warning': {
        'ru': '⚠️ Внимание!\n\n'
              'Вы сейчас заполняете форму заявки.\n'
              'Если вы смените язык, текущая форма будет сброшена и вам придется заполнить ее заново.\n\n'
              'Вы уверены, что хотите сменить язык?',
        'me': '⚠️ Upozorenje!\n\n'
              'Trenutno popunjavate formular zahtjeva.\n'
              'Ako promijenite jezik, trenutni formular će biti poništen i moraćete ga popuniti ponovo.\n\n'
              'Da li ste sigurni da želite promijeniti jezik?',
        'en': '⚠️ Warning!\n\n'
              'You are currently filling out a request form.\n'
              'If you change the language, the current form will be reset and you will have to fill it out again.\n\n'
              'Are you sure you want to change the language?',
    },
    
    'btn_confirm_language_change': {
        'ru': '✅ Да, сменить язык',
        'me': '✅ Da, promijeniti jezik',
        'en': '✅ Yes, change language',
    },
    
    'btn_continue_form': {
        'ru': '❌ Нет, продолжить заполнение',
        'me': '❌ Ne, nastaviti popunjavanje',
        'en': '❌ No, continue filling',
    },
}


def get_text(key: str, lang: str = 'en') -> str:
    """
    Получить текст по ключу и языку
    
    Args:
        key: Ключ текста
        lang: Код языка ('ru', 'me', 'en')
        
    Returns:
        Текст на выбранном языке или на английском (fallback)
    """
    # Проверяем, существует ли ключ
    if key not in TEXTS:
        return f"[Missing translation: {key}]"
    
    translations = TEXTS[key]
    
    # Возвращаем перевод на нужном языке или fallback на английский
    return translations.get(lang, translations.get('en', f"[No translation for {key}]"))


def format_text(key: str, lang: str = 'en', **kwargs) -> str:
    """
    Получить текст с подстановкой параметров
    
    Args:
        key: Ключ текста
        lang: Код языка
        **kwargs: Параметры для форматирования
        
    Returns:
        Отформатированный текст
    """
    text = get_text(key, lang)
    try:
        return text.format(**kwargs)
    except KeyError as e:
        return text  # Возвращаем неотформатированный текст в случае ошибки


# Список поддерживаемых языков
SUPPORTED_LANGUAGES = ['ru', 'me', 'en']

# Названия языков для кнопок
LANGUAGE_NAMES = {
    'ru': '🇷🇺 Русский',
    'me': '🇲🇪 Crnogorski',
    'en': '🇬🇧 English',
}
