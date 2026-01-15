# Production Deployment Guide

Полное руководство по развертыванию Telegram Lead Bot на продакшн-сервере.

## Содержание

1. [Настройка VPS](#настройка-vps)
2. [Развертывание с systemd](#развертывание-с-systemd)
3. [Развертывание с Docker](#развертывание-с-docker)
4. [Настройка backup'ов](#настройка-backupов)
5. [Мониторинг](#мониторинг)
6. [Безопасность](#безопасность)
7. [Обновление бота](#обновление-бота)

---

## Настройка VPS

### Минимальные требования

- **OS**: Ubuntu 20.04 LTS или выше (рекомендуется Ubuntu 22.04 LTS)
- **RAM**: 512 MB (рекомендуется 1 GB)
- **CPU**: 1 core
- **Disk**: 10 GB SSD
- **Network**: Стабильное подключение к интернету

### Начальная настройка сервера

#### 1. Обновление системы

```bash
sudo apt update && sudo apt upgrade -y
```

#### 2. Создание пользователя для бота

```bash
# Создать пользователя
sudo adduser botuser

# Добавить в группу sudo (опционально)
sudo usermod -aG sudo botuser

# Переключиться на пользователя
su - botuser
```

#### 3. Установка необходимых пакетов

```bash
# Python и зависимости
sudo apt install -y python3.11 python3.11-venv python3-pip git sqlite3

# Утилиты для мониторинга
sudo apt install -y htop curl wget
```

#### 4. Настройка SSH (рекомендуется)

```bash
# Генерация SSH ключа на локальной машине
ssh-keygen -t ed25519 -C "your_email@example.com"

# Копирование ключа на сервер
ssh-copy-id botuser@your_server_ip

# На сервере: отключить вход по паролю
sudo nano /etc/ssh/sshd_config
# Установить: PasswordAuthentication no
sudo systemctl restart sshd
```

#### 5. Настройка файрвола

```bash
# Разрешить SSH
sudo ufw allow 22/tcp

# Включить файрвол
sudo ufw enable

# Проверить статус
sudo ufw status
```

---

## Развертывание с systemd

### 1. Клонирование проекта

```bash
cd /home/botuser
git clone https://github.com/yourusername/telegram-lead-bot.git
cd telegram-lead-bot
```

### 2. Настройка окружения

```bash
# Создать виртуальное окружение
python3.11 -m venv venv

# Активировать
source venv/bin/activate

# Установить зависимости
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Настройка конфигурации

```bash
# Создать .env файл
nano .env
```

Содержимое `.env`:

```env
BOT_TOKEN=your_bot_token_from_botfather
ADMIN_CHAT_ID=your_telegram_chat_id
TIMEZONE=Europe/Podgorica
DB_PATH=/home/botuser/telegram-lead-bot/leads.db
```

**Важно**: Установите правильные права доступа:

```bash
chmod 600 .env
```

### 4. Тестовый запуск

```bash
# Запустить бота вручную для проверки
source venv/bin/activate
python -m app.bot
# Ctrl+C для остановки
```

### 5. Создание systemd service

```bash
sudo nano /etc/systemd/system/telegram-lead-bot.service
```

Содержимое файла:

```ini
[Unit]
Description=Telegram Lead Bot
After=network.target

[Service]
Type=simple
User=botuser
WorkingDirectory=/home/botuser/telegram-lead-bot
Environment="PATH=/home/botuser/telegram-lead-bot/venv/bin"
ExecStart=/home/botuser/telegram-lead-bot/venv/bin/python -m app.bot
Restart=always
RestartSec=10

# Логирование
StandardOutput=journal
StandardError=journal
SyslogIdentifier=telegram-lead-bot

# Безопасность
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=read-only
ReadWritePaths=/home/botuser/telegram-lead-bot

[Install]
WantedBy=multi-user.target
```

### 6. Запуск и автозагрузка

```bash
# Перезагрузить systemd
sudo systemctl daemon-reload

# Запустить бот
sudo systemctl start telegram-lead-bot

# Проверить статус
sudo systemctl status telegram-lead-bot

# Включить автозапуск при загрузке системы
sudo systemctl enable telegram-lead-bot
```

### 7. Управление сервисом

```bash
# Остановить
sudo systemctl stop telegram-lead-bot

# Перезапустить
sudo systemctl restart telegram-lead-bot

# Просмотр логов
sudo journalctl -u telegram-lead-bot -f

# Просмотр последних 100 строк логов
sudo journalctl -u telegram-lead-bot -n 100
```

---

## Развертывание с Docker

### 1. Установка Docker

```bash
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Добавить пользователя в группу docker
sudo usermod -aG docker botuser

# Перелогиниться для применения изменений
exit
su - botuser

# Установка Docker Compose
sudo apt install -y docker-compose-plugin
```

### 2. Создание Dockerfile

Создайте `Dockerfile` в корне проекта:

```dockerfile
FROM python:3.11-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Копирование зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование исходного кода
COPY app/ ./app/

# Создание директории для базы данных
RUN mkdir -p /data

# Переменная окружения для базы данных
ENV DB_PATH=/data/leads.db

# Запуск бота
CMD ["python", "-m", "app.bot"]
```

### 3. Создание docker-compose.yml

```yaml
version: '3.8'

services:
  telegram-bot:
    build: .
    container_name: telegram-lead-bot
    restart: unless-stopped
    env_file:
      - .env
    volumes:
      - ./data:/data
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"
    environment:
      - DB_PATH=/data/leads.db
```

### 4. Создание .env файла

```env
BOT_TOKEN=your_bot_token_from_botfather
ADMIN_CHAT_ID=your_telegram_chat_id
TIMEZONE=Europe/Podgorica
```

### 5. Создание .dockerignore

```
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
venv/
.env
.git/
.gitignore
*.md
*.db
.idea/
.vscode/
```

### 6. Запуск контейнера

```bash
# Создать директорию для данных
mkdir -p data

# Собрать и запустить
docker compose up -d

# Просмотр логов
docker compose logs -f

# Остановка
docker compose down

# Перезапуск
docker compose restart
```

### 7. Управление Docker контейнером

```bash
# Проверить статус
docker compose ps

# Просмотр логов
docker compose logs telegram-bot -f

# Войти в контейнер
docker compose exec telegram-bot bash

# Обновить контейнер
docker compose pull
docker compose up -d --build

# Очистить неиспользуемые образы
docker system prune -a
```

---

## Настройка backup'ов

### Автоматический backup базы данных

#### 1. Создание скрипта backup

```bash
mkdir -p /home/botuser/backups
nano /home/botuser/backup-bot.sh
```

Содержимое скрипта:

```bash
#!/bin/bash

# Конфигурация
BOT_DIR="/home/botuser/telegram-lead-bot"
DB_PATH="$BOT_DIR/leads.db"
BACKUP_DIR="/home/botuser/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/leads_backup_$DATE.db"
KEEP_DAYS=30

# Создать backup
sqlite3 "$DB_PATH" ".backup '$BACKUP_FILE'"

# Сжать backup
gzip "$BACKUP_FILE"

# Удалить старые backups (старше 30 дней)
find "$BACKUP_DIR" -name "leads_backup_*.db.gz" -mtime +$KEEP_DAYS -delete

echo "Backup completed: $BACKUP_FILE.gz"
```

Сделать скрипт исполняемым:

```bash
chmod +x /home/botuser/backup-bot.sh
```

#### 2. Настройка cron для автоматических backup'ов

```bash
crontab -e
```

Добавить строки для ежедневного backup в 3:00:

```cron
# Backup базы данных бота каждый день в 3:00
0 3 * * * /home/botuser/backup-bot.sh >> /home/botuser/backups/backup.log 2>&1
```

#### 3. Backup на удаленный сервер (опционально)

Используя `rsync` для копирования на другой сервер:

```bash
# Создать скрипт remote-backup.sh
nano /home/botuser/remote-backup.sh
```

```bash
#!/bin/bash

BACKUP_DIR="/home/botuser/backups"
REMOTE_USER="backupuser"
REMOTE_HOST="backup-server.example.com"
REMOTE_DIR="/backups/telegram-bot"

# Синхронизировать backups на удаленный сервер
rsync -avz --delete "$BACKUP_DIR/" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/"

echo "Remote backup completed"
```

```bash
chmod +x /home/botuser/remote-backup.sh

# Добавить в cron (после локального backup)
crontab -e
# 30 3 * * * /home/botuser/remote-backup.sh >> /home/botuser/backups/remote-backup.log 2>&1
```

#### 4. Восстановление из backup

```bash
# Остановить бота
sudo systemctl stop telegram-lead-bot

# Восстановить базу данных
cd /home/botuser/telegram-lead-bot
gunzip -c /home/botuser/backups/leads_backup_YYYYMMDD_HHMMSS.db.gz > leads.db

# Запустить бота
sudo systemctl start telegram-lead-bot
```

---

## Мониторинг

### 1. Мониторинг логов

#### Просмотр логов systemd

```bash
# Следить за логами в реальном времени
sudo journalctl -u telegram-lead-bot -f

# Последние 100 строк
sudo journalctl -u telegram-lead-bot -n 100

# Логи за сегодня
sudo journalctl -u telegram-lead-bot --since today

# Логи за последний час
sudo journalctl -u telegram-lead-bot --since "1 hour ago"

# Поиск ошибок
sudo journalctl -u telegram-lead-bot -p err
```

#### Просмотр логов Docker

```bash
# В реальном времени
docker compose logs -f telegram-bot

# Последние 100 строк
docker compose logs --tail 100 telegram-bot
```

### 2. Мониторинг ресурсов

```bash
# Использование CPU и памяти
htop

# Для Docker
docker stats telegram-lead-bot

# Использование диска
df -h
du -sh /home/botuser/telegram-lead-bot
```

### 3. Проверка доступности бота

Создайте простой скрипт мониторинга:

```bash
nano /home/botuser/check-bot.sh
```

```bash
#!/bin/bash

BOT_SERVICE="telegram-lead-bot"
ADMIN_EMAIL="admin@example.com"

# Проверка статуса сервиса
if ! systemctl is-active --quiet "$BOT_SERVICE"; then
    echo "Bot service is down! Attempting restart..." | mail -s "Bot Alert" "$ADMIN_EMAIL"
    sudo systemctl restart "$BOT_SERVICE"
    sleep 10
    
    if systemctl is-active --quiet "$BOT_SERVICE"; then
        echo "Bot successfully restarted" | mail -s "Bot Recovered" "$ADMIN_EMAIL"
    else
        echo "Failed to restart bot!" | mail -s "Bot CRITICAL" "$ADMIN_EMAIL"
    fi
fi
```

```bash
chmod +x /home/botuser/check-bot.sh

# Добавить в cron (проверка каждые 5 минут)
crontab -e
# */5 * * * * /home/botuser/check-bot.sh
```

### 4. Настройка alerts через Telegram

Создайте отдельный monitoring бот или используйте webhook для отправки критических уведомлений:

```bash
nano /home/botuser/telegram-alert.sh
```

```bash
#!/bin/bash

BOT_TOKEN="your_monitoring_bot_token"
CHAT_ID="your_admin_chat_id"
MESSAGE="$1"

curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
    -d chat_id="$CHAT_ID" \
    -d text="🚨 Alert: $MESSAGE" \
    -d parse_mode="HTML"
```

### 5. Мониторинг базы данных

```bash
# Размер базы данных
ls -lh /home/botuser/telegram-lead-bot/leads.db

# Количество записей
sqlite3 /home/botuser/telegram-lead-bot/leads.db "SELECT COUNT(*) FROM leads;"

# Последние 10 заявок
sqlite3 /home/botuser/telegram-lead-bot/leads.db "SELECT id, full_name, created_at FROM leads ORDER BY id DESC LIMIT 10;"
```

### 6. Внешний мониторинг (опционально)

Используйте сервисы для мониторинга uptime:
- [UptimeRobot](https://uptimerobot.com/) - бесплатный мониторинг до 50 сайтов
- [Pingdom](https://www.pingdom.com/)
- [StatusCake](https://www.statuscake.com/)

---

## Безопасность

### 1. Защита .env файла

```bash
# Установить правильные права доступа
chmod 600 /home/botuser/telegram-lead-bot/.env
chown botuser:botuser /home/botuser/telegram-lead-bot/.env

# Убедиться, что .env в .gitignore
echo ".env" >> .gitignore
```

### 2. Регулярные обновления системы

```bash
# Настроить автоматические обновления безопасности
sudo apt install unattended-upgrades
sudo dpkg-reconfigure --priority=low unattended-upgrades
```

### 3. Fail2ban для защиты SSH

```bash
# Установить Fail2ban
sudo apt install fail2ban

# Создать локальную конфигурацию
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local

# Настроить для SSH:
# [sshd]
# enabled = true
# maxretry = 3
# bantime = 3600

# Запустить сервис
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Проверить статус
sudo fail2ban-client status sshd
```

### 4. Регулярный аудит логов

```bash
# Создать скрипт проверки подозрительной активности
nano /home/botuser/security-check.sh
```

```bash
#!/bin/bash

echo "=== Failed login attempts ==="
sudo grep "Failed password" /var/log/auth.log | tail -10

echo "=== Bot errors ==="
sudo journalctl -u telegram-lead-bot -p err --since "1 day ago"

echo "=== Disk usage ==="
df -h | grep -v tmpfs
```

### 5. Ограничение доступа к базе данных

```bash
# Установить права доступа
chmod 600 /home/botuser/telegram-lead-bot/leads.db
chown botuser:botuser /home/botuser/telegram-lead-bot/leads.db
```

---

## Обновление бота

### Процедура обновления (systemd)

```bash
# 1. Перейти в директорию проекта
cd /home/botuser/telegram-lead-bot

# 2. Сделать backup базы данных
/home/botuser/backup-bot.sh

# 3. Остановить бота
sudo systemctl stop telegram-lead-bot

# 4. Получить обновления из git
git pull origin main

# 5. Обновить зависимости (если изменились)
source venv/bin/activate
pip install --upgrade -r requirements.txt

# 6. Проверить миграции базы данных (если есть)
# python -m app.migrate  # если есть скрипт миграций

# 7. Запустить бота
sudo systemctl start telegram-lead-bot

# 8. Проверить статус
sudo systemctl status telegram-lead-bot

# 9. Проверить логи
sudo journalctl -u telegram-lead-bot -f
```

### Процедура обновления (Docker)

```bash
# 1. Перейти в директорию проекта
cd /home/botuser/telegram-lead-bot

# 2. Сделать backup базы данных
/home/botuser/backup-bot.sh

# 3. Получить обновления
git pull origin main

# 4. Пересобрать и перезапустить контейнер
docker compose down
docker compose up -d --build

# 5. Проверить логи
docker compose logs -f
```

### Откат к предыдущей версии

```bash
# systemd
cd /home/botuser/telegram-lead-bot
sudo systemctl stop telegram-lead-bot
git reset --hard HEAD~1  # или конкретный коммит
sudo systemctl start telegram-lead-bot

# Docker
cd /home/botuser/telegram-lead-bot
docker compose down
git reset --hard HEAD~1
docker compose up -d --build
```

---

## Дополнительные рекомендации

### 1. Настройка логирования в файл

Если хотите дополнительное логирование в файл, добавьте в `app/bot.py`:

```python
import logging
from logging.handlers import RotatingFileHandler

# Настройка file handler
file_handler = RotatingFileHandler(
    'bot.log',
    maxBytes=10*1024*1024,  # 10 MB
    backupCount=5
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))

logging.getLogger().addHandler(file_handler)
```

### 2. Тестирование на staging окружении

Рекомендуется создать отдельного тестового бота для staging:

```bash
# Клонировать в отдельную директорию
git clone https://github.com/yourusername/telegram-lead-bot.git telegram-lead-bot-staging
cd telegram-lead-bot-staging

# Создать отдельный .env с токеном тестового бота
nano .env

# Запустить на другом порту или с другим именем сервиса
sudo nano /etc/systemd/system/telegram-lead-bot-staging.service
```

### 3. Мониторинг производительности

```bash
# Установить atop для детального мониторинга
sudo apt install atop

# Запустить atop
sudo systemctl enable atop
sudo systemctl start atop

# Просмотр логов atop
atop -r /var/log/atop/atop_$(date +%Y%m%d)
```

---

## Контрольный список перед запуском в продакшн

- [ ] VPS настроен и обновлен
- [ ] Создан отдельный пользователь для бота
- [ ] Настроен SSH с ключами (пароли отключены)
- [ ] Настроен файрвол (ufw)
- [ ] Python 3.11+ установлен
- [ ] Все зависимости установлены
- [ ] .env файл создан с правильными правами (600)
- [ ] BOT_TOKEN и ADMIN_CHAT_ID настроены
- [ ] База данных инициализирована
- [ ] Systemd service или Docker настроен
- [ ] Автозапуск при загрузке системы включен
- [ ] Backup скрипты настроены и протестированы
- [ ] Cron задачи для backup'ов добавлены
- [ ] Мониторинг логов настроен
- [ ] Alerts настроены (опционально)
- [ ] Fail2ban установлен и настроен
- [ ] Автоматические обновления безопасности включены
- [ ] Процедура обновления протестирована
- [ ] Процедура отката протестирована
- [ ] Документация актуальна

---

## Полезные команды

```bash
# Проверка статуса бота
sudo systemctl status telegram-lead-bot

# Просмотр логов
sudo journalctl -u telegram-lead-bot -f

# Перезапуск бота
sudo systemctl restart telegram-lead-bot

# Проверка использования ресурсов
htop

# Размер базы данных
ls -lh /home/botuser/telegram-lead-bot/leads.db

# Backup базы данных
/home/botuser/backup-bot.sh

# Проверка доступного места на диске
df -h

# Список backup'ов
ls -lh /home/botuser/backups/
```

---

## Поддержка

При возникновении проблем:

1. Проверьте логи: `sudo journalctl -u telegram-lead-bot -n 100`
2. Проверьте статус сервиса: `sudo systemctl status telegram-lead-bot`
3. Проверьте конфигурацию: `cat .env` (осторожно с токеном!)
4. Проверьте права доступа к файлам
5. Убедитесь, что база данных доступна и не повреждена

Для получения дополнительной помощи обратитесь к документации проекта или создайте issue в репозитории.
