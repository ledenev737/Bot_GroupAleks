#!/bin/bash

# Скрипт синхронизации backup'ов на удаленный сервер
# Использование: ./remote-backup.sh

# КОНФИГУРАЦИЯ - ИЗМЕНИТЕ ПОД СВОИ НУЖДЫ
REMOTE_USER="backupuser"
REMOTE_HOST="backup-server.example.com"
REMOTE_DIR="/backups/telegram-bot"

# Локальная конфигурация
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
BACKUP_DIR="$PROJECT_DIR/backups"

# Проверка наличия rsync
if ! command -v rsync &> /dev/null; then
    echo "Error: rsync not installed"
    echo "Install it with: sudo apt install rsync"
    exit 1
fi

# Проверка наличия локальных backup'ов
if [ ! -d "$BACKUP_DIR" ] || [ -z "$(ls -A "$BACKUP_DIR")" ]; then
    echo "Error: No backups found in $BACKUP_DIR"
    exit 1
fi

echo "=== Remote Backup Sync ==="
echo "Local directory: $BACKUP_DIR"
echo "Remote: $REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR"
echo ""

# Тест соединения с удаленным сервером
echo "Testing connection to remote server..."
if ! ssh -o ConnectTimeout=10 "$REMOTE_USER@$REMOTE_HOST" "exit" 2>/dev/null; then
    echo "Error: Cannot connect to remote server"
    echo "Make sure SSH keys are configured and server is accessible"
    exit 1
fi

echo "Connection successful!"
echo ""

# Создать удаленную директорию, если не существует
echo "Creating remote directory if needed..."
ssh "$REMOTE_USER@$REMOTE_HOST" "mkdir -p $REMOTE_DIR"

# Синхронизировать backups
echo "Syncing backups..."
rsync -avz --progress \
    --delete \
    --backup --backup-dir="$REMOTE_DIR/deleted_$(date +%Y%m%d)" \
    "$BACKUP_DIR/" \
    "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/"

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Remote backup sync completed successfully!"
    
    # Показать статистику на удаленном сервере
    echo ""
    echo "Remote backup statistics:"
    ssh "$REMOTE_USER@$REMOTE_HOST" "du -sh $REMOTE_DIR && ls -lh $REMOTE_DIR/*.db.gz 2>/dev/null | wc -l | xargs echo 'Total files:'"
else
    echo ""
    echo "✗ Error: Remote backup sync failed"
    exit 1
fi
