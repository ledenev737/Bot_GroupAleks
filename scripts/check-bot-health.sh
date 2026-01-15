#!/bin/bash

# Скрипт проверки работоспособности бота
# Использование: ./check-bot-health.sh

# Конфигурация
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
DB_PATH="$PROJECT_DIR/leads.db"
SERVICE_NAME="telegram-lead-bot"

echo "=== Telegram Lead Bot Health Check ==="
echo "Date: $(date)"
echo ""

# Проверка 1: Systemd Service
echo "1. Checking systemd service..."
if command -v systemctl &> /dev/null; then
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        echo "   ✓ Service is running"
        SERVICE_STATUS=$(systemctl show -p ActiveState -p SubState --value "$SERVICE_NAME" | tr '\n' ' ')
        echo "   Status: $SERVICE_STATUS"
    else
        echo "   ✗ Service is NOT running"
        echo "   Attempting to restart..."
        sudo systemctl restart "$SERVICE_NAME"
        sleep 3
        if systemctl is-active --quiet "$SERVICE_NAME"; then
            echo "   ✓ Service restarted successfully"
        else
            echo "   ✗ Failed to restart service"
        fi
    fi
else
    echo "   - Systemd not available, skipping..."
fi
echo ""

# Проверка 2: Docker Container
echo "2. Checking Docker container..."
if command -v docker &> /dev/null; then
    CONTAINER_STATUS=$(docker inspect -f '{{.State.Status}}' telegram-lead-bot 2>/dev/null)
    if [ "$CONTAINER_STATUS" == "running" ]; then
        echo "   ✓ Container is running"
        echo "   Status: $CONTAINER_STATUS"
    else
        echo "   ✗ Container is NOT running (Status: $CONTAINER_STATUS)"
    fi
else
    echo "   - Docker not available, skipping..."
fi
echo ""

# Проверка 3: База данных
echo "3. Checking database..."
if [ -f "$DB_PATH" ]; then
    echo "   ✓ Database file exists"
    DB_SIZE=$(du -h "$DB_PATH" | cut -f1)
    echo "   Size: $DB_SIZE"
    
    # Проверить целостность базы данных
    if command -v sqlite3 &> /dev/null; then
        INTEGRITY=$(sqlite3 "$DB_PATH" "PRAGMA integrity_check;" 2>&1)
        if [ "$INTEGRITY" == "ok" ]; then
            echo "   ✓ Database integrity OK"
        else
            echo "   ✗ Database integrity check failed: $INTEGRITY"
        fi
        
        # Статистика
        LEADS_COUNT=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM leads;" 2>/dev/null)
        USERS_COUNT=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM users;" 2>/dev/null)
        echo "   Leads: $LEADS_COUNT"
        echo "   Users: $USERS_COUNT"
    fi
else
    echo "   ✗ Database file not found: $DB_PATH"
fi
echo ""

# Проверка 4: Логи
echo "4. Checking recent logs..."
if command -v journalctl &> /dev/null; then
    echo "   Recent errors (last 24 hours):"
    ERROR_COUNT=$(journalctl -u "$SERVICE_NAME" --since "24 hours ago" -p err --no-pager 2>/dev/null | wc -l)
    echo "   Error count: $ERROR_COUNT"
    
    if [ "$ERROR_COUNT" -gt 0 ]; then
        echo "   Last 5 errors:"
        journalctl -u "$SERVICE_NAME" --since "24 hours ago" -p err --no-pager -n 5 2>/dev/null | sed 's/^/   /'
    fi
fi
echo ""

# Проверка 5: Ресурсы
echo "5. Checking system resources..."
if command -v free &> /dev/null; then
    MEMORY=$(free -h | awk '/^Mem:/ {print $3 "/" $2}')
    echo "   Memory used: $MEMORY"
fi

if command -v df &> /dev/null; then
    DISK=$(df -h "$PROJECT_DIR" | awk 'NR==2 {print $3 "/" $2 " (" $5 " used)"}')
    echo "   Disk used: $DISK"
fi
echo ""

# Проверка 6: Backups
echo "6. Checking backups..."
BACKUP_DIR="$PROJECT_DIR/backups"
if [ -d "$BACKUP_DIR" ]; then
    BACKUP_COUNT=$(find "$BACKUP_DIR" -name "leads_backup_*.db.gz" 2>/dev/null | wc -l)
    echo "   Total backups: $BACKUP_COUNT"
    
    if [ "$BACKUP_COUNT" -gt 0 ]; then
        LATEST_BACKUP=$(ls -t "$BACKUP_DIR"/leads_backup_*.db.gz 2>/dev/null | head -1)
        if [ -n "$LATEST_BACKUP" ]; then
            LATEST_DATE=$(stat -c %y "$LATEST_BACKUP" 2>/dev/null | cut -d' ' -f1)
            echo "   Latest backup: $(basename "$LATEST_BACKUP")"
            echo "   Date: $LATEST_DATE"
        fi
    else
        echo "   ⚠ No backups found"
    fi
else
    echo "   ⚠ Backup directory not found"
fi
echo ""

# Итоговый статус
echo "=== Health Check Complete ==="
