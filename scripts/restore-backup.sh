#!/bin/bash

# Скрипт восстановления базы данных из backup
# Использование: ./restore-backup.sh /path/to/backup.db.gz

# Конфигурация
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DB_PATH="$PROJECT_DIR/leads.db"

# Проверка аргументов
if [ $# -eq 0 ]; then
    echo "Usage: $0 <backup_file.db.gz>"
    echo ""
    echo "Available backups:"
    ls -lh "$PROJECT_DIR/backups/"*.db.gz 2>/dev/null || echo "No backups found"
    exit 1
fi

BACKUP_FILE="$1"

# Проверить, существует ли файл backup
if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file not found: $BACKUP_FILE"
    exit 1
fi

# Предупреждение
echo "WARNING: This will replace the current database!"
echo "Current database: $DB_PATH"
echo "Backup file: $BACKUP_FILE"
echo ""
read -p "Are you sure you want to continue? (yes/no): " confirmation

if [ "$confirmation" != "yes" ]; then
    echo "Restore cancelled."
    exit 0
fi

# Создать backup текущей базы данных
if [ -f "$DB_PATH" ]; then
    CURRENT_BACKUP="$DB_PATH.before_restore.$(date +%Y%m%d_%H%M%S).db"
    echo "Creating backup of current database: $CURRENT_BACKUP"
    cp "$DB_PATH" "$CURRENT_BACKUP"
fi

# Остановить бота (если используется systemd)
echo "Stopping bot service..."
if command -v systemctl &> /dev/null; then
    sudo systemctl stop telegram-lead-bot 2>/dev/null || echo "Service not running or not using systemd"
fi

# Или остановить Docker контейнер
if command -v docker &> /dev/null; then
    cd "$PROJECT_DIR"
    docker compose stop 2>/dev/null || echo "Docker container not running"
fi

# Распаковать и восстановить базу данных
echo "Restoring database from backup..."
gunzip -c "$BACKUP_FILE" > "$DB_PATH"

if [ $? -eq 0 ]; then
    echo "Database restored successfully!"
    
    # Запустить бота обратно
    echo "Starting bot service..."
    if command -v systemctl &> /dev/null; then
        sudo systemctl start telegram-lead-bot 2>/dev/null
    fi
    
    if command -v docker &> /dev/null; then
        cd "$PROJECT_DIR"
        docker compose start 2>/dev/null
    fi
    
    echo "Restore completed!"
else
    echo "Error: Failed to restore database"
    
    # Восстановить предыдущую версию
    if [ -f "$CURRENT_BACKUP" ]; then
        echo "Restoring previous version..."
        cp "$CURRENT_BACKUP" "$DB_PATH"
    fi
    
    exit 1
fi
