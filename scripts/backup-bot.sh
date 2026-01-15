#!/bin/bash

# Скрипт автоматического backup базы данных бота
# Использование: ./backup-bot.sh

# Конфигурация
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DB_PATH="$PROJECT_DIR/leads.db"
BACKUP_DIR="$PROJECT_DIR/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/leads_backup_$DATE.db"
KEEP_DAYS=30

# Создать директорию для backup'ов, если не существует
mkdir -p "$BACKUP_DIR"

# Проверить, существует ли база данных
if [ ! -f "$DB_PATH" ]; then
    echo "Error: Database not found at $DB_PATH"
    exit 1
fi

# Создать backup
echo "Creating backup: $BACKUP_FILE"
sqlite3 "$DB_PATH" ".backup '$BACKUP_FILE'"

if [ $? -eq 0 ]; then
    # Сжать backup
    echo "Compressing backup..."
    gzip "$BACKUP_FILE"
    
    if [ $? -eq 0 ]; then
        echo "Backup completed successfully: $BACKUP_FILE.gz"
        
        # Удалить старые backups (старше указанного количества дней)
        echo "Cleaning old backups (older than $KEEP_DAYS days)..."
        find "$BACKUP_DIR" -name "leads_backup_*.db.gz" -mtime +$KEEP_DAYS -delete
        
        # Показать статистику
        BACKUP_COUNT=$(find "$BACKUP_DIR" -name "leads_backup_*.db.gz" | wc -l)
        BACKUP_SIZE=$(du -sh "$BACKUP_DIR" | cut -f1)
        echo "Total backups: $BACKUP_COUNT"
        echo "Total size: $BACKUP_SIZE"
    else
        echo "Error: Failed to compress backup"
        exit 1
    fi
else
    echo "Error: Failed to create backup"
    exit 1
fi
