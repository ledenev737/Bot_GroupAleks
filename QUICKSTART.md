# Quick Start Guide

Краткое руководство по развертыванию Telegram Lead Bot.

## Развертывание на локальной машине (для разработки)

### 1. Клонировать репозиторий

```bash
git clone https://github.com/yourusername/telegram-lead-bot.git
cd telegram-lead-bot
```

### 2. Создать виртуальное окружение

```bash
python -m venv venv

# Windows PowerShell
venv\Scripts\Activate.ps1

# Linux/Mac
source venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install -r requirements.txt
```

### 4. Настроить .env файл

Создайте файл `.env` в корне проекта:

```env
BOT_TOKEN=your_bot_token_from_botfather
ADMIN_CHAT_ID=your_telegram_chat_id
TIMEZONE=Europe/Podgorica
```

**Как получить BOT_TOKEN:**
1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте `/newbot` и следуйте инструкциям
3. Скопируйте полученный токен

**Как получить ADMIN_CHAT_ID:**
1. Найдите [@userinfobot](https://t.me/userinfobot) в Telegram
2. Отправьте любое сообщение
3. Скопируйте ваш ID (число)

### 5. Запустить бота

```bash
python -m app.bot
```

Готово! Бот запущен. Найдите его в Telegram и отправьте `/start`.

---

## Развертывание на VPS (Production)

### Вариант 1: Systemd Service (рекомендуется)

**Шаг 1: Подготовка сервера**

```bash
# Обновить систему
sudo apt update && sudo apt upgrade -y

# Установить необходимые пакеты
sudo apt install -y python3.11 python3.11-venv git sqlite3

# Создать пользователя
sudo adduser botuser
sudo su - botuser
```

**Шаг 2: Клонировать и настроить**

```bash
cd /home/botuser
git clone https://github.com/yourusername/telegram-lead-bot.git
cd telegram-lead-bot

# Создать виртуальное окружение
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Настроить .env
nano .env
# Вставить: BOT_TOKEN, ADMIN_CHAT_ID, TIMEZONE
chmod 600 .env
```

**Шаг 3: Создать systemd service**

```bash
# Скопировать шаблон service файла
sudo cp scripts/telegram-lead-bot.service /etc/systemd/system/

# Отредактировать пути (если нужно)
sudo nano /etc/systemd/system/telegram-lead-bot.service

# ВАЖНО: Убедитесь, что User и WorkingDirectory правильные!
```

**Шаг 4: Запустить и включить автозапуск**

```bash
sudo systemctl daemon-reload
sudo systemctl start telegram-lead-bot
sudo systemctl enable telegram-lead-bot

# Проверить статус
sudo systemctl status telegram-lead-bot

# Просмотр логов
sudo journalctl -u telegram-lead-bot -f
```

**Шаг 5: Настроить backup'ы**

```bash
# Сделать скрипты исполняемыми
chmod +x scripts/*.sh

# Добавить в crontab
crontab -e

# Добавить строку:
# 0 3 * * * /home/botuser/telegram-lead-bot/scripts/backup-bot.sh >> /home/botuser/backups/backup.log 2>&1
```

**Готово!** Бот работает и автоматически перезапустится при перезагрузке сервера.

---

### Вариант 2: Docker (альтернатива)

**Шаг 1: Установить Docker**

```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Добавить пользователя в группу docker
sudo usermod -aG docker $USER

# Перелогиниться
exit
# Войти снова
```

**Шаг 2: Клонировать и настроить**

```bash
git clone https://github.com/yourusername/telegram-lead-bot.git
cd telegram-lead-bot

# Создать .env файл
nano .env
# Вставить: BOT_TOKEN, ADMIN_CHAT_ID, TIMEZONE

# Создать директорию для данных
mkdir -p data
```

**Шаг 3: Запустить контейнер**

```bash
# Собрать и запустить
docker compose up -d

# Проверить статус
docker compose ps

# Просмотр логов
docker compose logs -f
```

**Шаг 4: Настроить backup'ы**

```bash
# Изменить путь к базе данных в скрипте
nano scripts/backup-bot.sh
# DB_PATH="$BOT_DIR/data/leads.db"

# Сделать исполняемым и добавить в cron
chmod +x scripts/backup-bot.sh
crontab -e
# 0 3 * * * /path/to/telegram-lead-bot/scripts/backup-bot.sh >> /path/to/backups/backup.log 2>&1
```

**Готово!** Бот работает в контейнере.

---

## Основные команды управления

### Systemd

```bash
# Запустить
sudo systemctl start telegram-lead-bot

# Остановить
sudo systemctl stop telegram-lead-bot

# Перезапустить
sudo systemctl restart telegram-lead-bot

# Статус
sudo systemctl status telegram-lead-bot

# Логи
sudo journalctl -u telegram-lead-bot -f

# Отключить автозапуск
sudo systemctl disable telegram-lead-bot
```

### Docker

```bash
# Запустить
docker compose up -d

# Остановить
docker compose down

# Перезапустить
docker compose restart

# Статус
docker compose ps

# Логи
docker compose logs -f

# Пересобрать
docker compose up -d --build
```

---

## Обновление бота

### Systemd

```bash
cd /home/botuser/telegram-lead-bot

# Остановить бота
sudo systemctl stop telegram-lead-bot

# Обновить код
git pull origin main

# Обновить зависимости (если нужно)
source venv/bin/activate
pip install --upgrade -r requirements.txt

# Запустить
sudo systemctl start telegram-lead-bot
```

### Docker

```bash
cd /path/to/telegram-lead-bot

# Остановить
docker compose down

# Обновить код
git pull origin main

# Пересобрать и запустить
docker compose up -d --build
```

---

## Резервное копирование и восстановление

### Создать backup

```bash
./scripts/backup-bot.sh
```

### Восстановить из backup

```bash
./scripts/restore-backup.sh /path/to/backup.db.gz
```

### Автоматические backup'ы

```bash
crontab -e

# Ежедневно в 3:00
0 3 * * * /path/to/scripts/backup-bot.sh >> /path/to/backups/backup.log 2>&1
```

---

## Проверка работоспособности

### Проверка статуса

```bash
./scripts/check-bot-health.sh
```

### Просмотр базы данных

```bash
sqlite3 leads.db

# Количество заявок
SELECT COUNT(*) FROM leads;

# Последние 10 заявок
SELECT id, full_name, phone, created_at FROM leads ORDER BY id DESC LIMIT 10;

# Выход
.exit
```

---

## Устранение проблем

### Бот не запускается

```bash
# Проверить логи
sudo journalctl -u telegram-lead-bot -n 50

# Проверить .env файл
cat .env

# Проверить права доступа
ls -la leads.db
ls -la .env

# Попробовать запустить вручную
source venv/bin/activate
python -m app.bot
```

### Бот не отвечает

1. Проверить, запущен ли процесс: `sudo systemctl status telegram-lead-bot`
2. Проверить логи на ошибки
3. Проверить токен бота в BotFather
4. Убедиться, что бот не заблокирован

### Ошибки базы данных

```bash
# Проверить целостность
sqlite3 leads.db "PRAGMA integrity_check;"

# Если повреждена, восстановить из backup
./scripts/restore-backup.sh /path/to/backup.db.gz
```

---

## Безопасность

### Базовые меры безопасности

```bash
# Права доступа
chmod 600 .env
chmod 600 leads.db

# Файрвол
sudo ufw allow 22/tcp
sudo ufw enable

# Автоматические обновления
sudo apt install unattended-upgrades
sudo dpkg-reconfigure --priority=low unattended-upgrades

# SSH ключи (рекомендуется)
ssh-keygen -t ed25519
ssh-copy-id user@your-server

# Отключить вход по паролю
sudo nano /etc/ssh/sshd_config
# PasswordAuthentication no
sudo systemctl restart sshd
```

---

## Полезные ссылки

- [DEPLOYMENT.md](DEPLOYMENT.md) - Подробное руководство по развертыванию
- [README.md](README.md) - Основная документация
- [scripts/README.md](scripts/README.md) - Документация по скриптам
- [AI_ENHANCEMENT.md](AI_ENHANCEMENT.md) - AI функции бота
- [NEW_FEATURES.md](NEW_FEATURES.md) - Новые возможности

---

## Получение помощи

При возникновении проблем:

1. Проверьте [DEPLOYMENT.md](DEPLOYMENT.md) для детальной информации
2. Просмотрите логи: `sudo journalctl -u telegram-lead-bot -n 100`
3. Проверьте статус: `sudo systemctl status telegram-lead-bot`
4. Запустите health check: `./scripts/check-bot-health.sh`
5. Создайте issue в репозитории GitHub

---

## Контрольный список

Перед запуском в продакшн убедитесь:

- [ ] BOT_TOKEN настроен правильно
- [ ] ADMIN_CHAT_ID настроен правильно
- [ ] Файрвол настроен
- [ ] SSH ключи настроены (пароли отключены)
- [ ] Автоматические backup'ы настроены
- [ ] Сервис автоматически запускается при перезагрузке
- [ ] Логи мониторятся
- [ ] .env файл защищен (chmod 600)
- [ ] База данных защищена (chmod 600)
- [ ] Автоматические обновления безопасности включены

**Готово!** Ваш бот готов к работе в продакшн! 🚀
