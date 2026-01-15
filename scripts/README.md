# Скрипты автоматизации

Эта папка содержит скрипты для автоматизации управления ботом в продакшн-окружении.

## Список скриптов

### 1. backup-bot.sh

Автоматическое создание backup базы данных.

**Использование:**
```bash
./scripts/backup-bot.sh
```

**Что делает:**
- Создает backup базы данных SQLite
- Сжимает backup с помощью gzip
- Удаляет старые backup'ы (старше 30 дней)
- Показывает статистику

**Автоматизация:**
```bash
# Добавить в crontab для ежедневного backup в 3:00
crontab -e
# 0 3 * * * /path/to/scripts/backup-bot.sh >> /path/to/backups/backup.log 2>&1
```

---

### 2. restore-backup.sh

Восстановление базы данных из backup.

**Использование:**
```bash
./scripts/restore-backup.sh /path/to/backup.db.gz
```

**Что делает:**
- Останавливает бота
- Создает backup текущей базы данных
- Восстанавливает базу из указанного backup'а
- Запускает бота обратно

**Осторожно:** Заменяет текущую базу данных!

---

### 3. check-bot-health.sh

Проверка состояния бота и системы.

**Использование:**
```bash
./scripts/check-bot-health.sh
```

**Что проверяет:**
- Статус systemd service или Docker контейнера
- Целостность и размер базы данных
- Количество записей (leads, users)
- Последние ошибки в логах
- Использование системных ресурсов (память, диск)
- Наличие и актуальность backup'ов

**Автоматизация:**
```bash
# Проверка каждые 5 минут
crontab -e
# */5 * * * * /path/to/scripts/check-bot-health.sh >> /path/to/health-check.log 2>&1
```

---

### 4. remote-backup.sh

Синхронизация backup'ов на удаленный сервер.

**Использование:**
```bash
# 1. Настроить параметры в скрипте
nano scripts/remote-backup.sh
# Изменить: REMOTE_USER, REMOTE_HOST, REMOTE_DIR

# 2. Настроить SSH ключи
ssh-copy-id backupuser@backup-server.example.com

# 3. Запустить
./scripts/remote-backup.sh
```

**Что делает:**
- Проверяет соединение с удаленным сервером
- Синхронизирует локальные backup'ы на удаленный сервер
- Создает архив удаленных файлов
- Показывает статистику

**Автоматизация:**
```bash
# Синхронизация после каждого backup (в 3:30)
crontab -e
# 30 3 * * * /path/to/scripts/remote-backup.sh >> /path/to/remote-backup.log 2>&1
```

---

### 5. telegram-alert.sh

Отправка уведомлений в Telegram.

**Использование:**
```bash
# 1. Настроить параметры в скрипте
nano scripts/telegram-alert.sh
# Изменить: BOT_TOKEN, CHAT_ID

# 2. Отправить уведомление
./scripts/telegram-alert.sh "Важное сообщение"
```

**Что делает:**
- Отправляет форматированное сообщение в Telegram
- Включает информацию о сервере и времени
- Можно интегрировать с другими скриптами для alert'ов

**Пример интеграции:**
```bash
# В других скриптах
if [ $ERROR_OCCURRED ]; then
    ./scripts/telegram-alert.sh "Bot service is down!"
fi
```

---

## Установка и настройка

### 1. Сделать скрипты исполняемыми

```bash
chmod +x scripts/*.sh
```

### 2. Проверить зависимости

```bash
# Убедиться, что установлены необходимые утилиты
sudo apt install sqlite3 rsync curl
```

### 3. Настроить переменные окружения

В скриптах `remote-backup.sh` и `telegram-alert.sh` нужно настроить параметры:

- **remote-backup.sh**: REMOTE_USER, REMOTE_HOST, REMOTE_DIR
- **telegram-alert.sh**: BOT_TOKEN, CHAT_ID (или использовать .env файл)

### 4. Настроить автоматизацию (cron)

Пример полной конфигурации cron:

```bash
crontab -e
```

```cron
# Backup базы данных каждый день в 3:00
0 3 * * * /home/botuser/telegram-lead-bot/scripts/backup-bot.sh >> /home/botuser/backups/backup.log 2>&1

# Синхронизация на удаленный сервер в 3:30
30 3 * * * /home/botuser/telegram-lead-bot/scripts/remote-backup.sh >> /home/botuser/backups/remote-backup.log 2>&1

# Проверка здоровья бота каждые 5 минут
*/5 * * * * /home/botuser/telegram-lead-bot/scripts/check-bot-health.sh >> /home/botuser/health-check.log 2>&1
```

---

## Безопасность

### Права доступа

```bash
# Установить правильные права на скрипты
chmod 750 scripts/*.sh

# Защитить логи
chmod 640 /path/to/logs/*.log
```

### SSH ключи для remote backup

```bash
# Генерировать отдельный ключ для backup'ов
ssh-keygen -t ed25519 -f ~/.ssh/backup_key -C "backup-bot"

# Добавить на удаленный сервер
ssh-copy-id -i ~/.ssh/backup_key backupuser@backup-server.example.com

# Использовать в скрипте
ssh -i ~/.ssh/backup_key backupuser@backup-server.example.com
```

---

## Мониторинг логов

### Просмотр логов cron

```bash
# Логи backup
tail -f /home/botuser/backups/backup.log

# Логи health check
tail -f /home/botuser/health-check.log

# Логи remote backup
tail -f /home/botuser/backups/remote-backup.log
```

### Алерты при ошибках

Можно настроить отправку alert'ов при ошибках:

```bash
# В конце скрипта backup-bot.sh
if [ $? -ne 0 ]; then
    /path/to/scripts/telegram-alert.sh "Backup failed!"
fi
```

---

## Устранение проблем

### Скрипт не выполняется в cron

1. Проверить права доступа
2. Использовать абсолютные пути
3. Проверить переменные окружения
4. Проверить логи: `grep CRON /var/log/syslog`

### Remote backup не работает

1. Проверить SSH соединение: `ssh user@host`
2. Проверить права доступа на удаленном сервере
3. Убедиться, что rsync установлен на обоих серверах

### Telegram alerts не отправляются

1. Проверить BOT_TOKEN и CHAT_ID
2. Убедиться, что бот добавлен в чат
3. Проверить интернет-соединение
4. Протестировать вручную: `curl https://api.telegram.org/bot<TOKEN>/getMe`

---

## Дополнительные ресурсы

Для получения дополнительной информации см.:

- [DEPLOYMENT.md](../DEPLOYMENT.md) - Полное руководство по развертыванию
- [README.md](../README.md) - Основная документация проекта
- [cron documentation](https://man7.org/linux/man-pages/man5/crontab.5.html) - Документация по cron
