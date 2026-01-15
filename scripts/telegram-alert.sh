#!/bin/bash

# Скрипт отправки уведомлений в Telegram
# Использование: ./telegram-alert.sh "Your message here"

# КОНФИГУРАЦИЯ - ИЗМЕНИТЕ ПОД СВОИ НУЖДЫ
# Можно использовать отдельного бота для мониторинга
BOT_TOKEN="your_monitoring_bot_token_here"
CHAT_ID="your_admin_chat_id_here"

# Или загрузить из .env файла
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
ENV_FILE="$PROJECT_DIR/.env"

if [ -f "$ENV_FILE" ]; then
    # Попытаться загрузить настройки из .env
    source <(grep -E '^(BOT_TOKEN|ADMIN_CHAT_ID)=' "$ENV_FILE" | sed 's/^/export /')
fi

# Проверка аргументов
if [ $# -eq 0 ]; then
    echo "Usage: $0 \"Your alert message\""
    exit 1
fi

MESSAGE="$1"
HOSTNAME=$(hostname)
DATE=$(date "+%Y-%m-%d %H:%M:%S")

# Форматированное сообщение
FORMATTED_MESSAGE="🚨 <b>Alert</b>

<b>Server:</b> $HOSTNAME
<b>Time:</b> $DATE

<b>Message:</b>
$MESSAGE"

# Отправка сообщения
RESPONSE=$(curl -s -X POST "https://api.telegram.org/bot$BOT_TOKEN/sendMessage" \
    -d chat_id="$CHAT_ID" \
    -d text="$FORMATTED_MESSAGE" \
    -d parse_mode="HTML")

# Проверка результата
if echo "$RESPONSE" | grep -q '"ok":true'; then
    echo "✓ Alert sent successfully"
    exit 0
else
    echo "✗ Failed to send alert"
    echo "Response: $RESPONSE"
    exit 1
fi
