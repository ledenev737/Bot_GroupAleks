# Telegram Lead Bot

## Purpose

This document explains how to install, configure, and run a Telegram bot that collects construction project leads from clients in three languages: Russian, Montenegrin, and English.

## Audience

- Developers setting up the bot
- System administrators deploying to production

## Bot Link

[@GroupAleksDOO_bot](https://t.me/GroupAleksDOO_bot)

## Features

- Multi-language interface (Russian, Montenegrin, English)
- Step-by-step lead collection form
- Phone and email validation
- SQLite data storage
- Admin notifications via Telegram (with Telegram ID)
- FSM (Finite State Machine) for conversation flow
- **🤖 AI-powered description enhancement** - automatically structures and improves project descriptions
- **📎 File attachments** - users can upload photos, documents, and videos
- **🔄 Smart repeat applications** - reuses contact data from previous submissions

## Installation

### Prerequisites

- Python 3.11 or higher
- Telegram account

### Step 1: Get Bot Token

1. Open Telegram and find [@BotFather](https://t.me/BotFather)
2. Send command `/newbot`
3. Follow instructions to create bot
4. Copy the token (format: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 2: Get Admin Chat ID

Option 1 (Recommended):
1. Find [@userinfobot](https://t.me/userinfobot) in Telegram
2. Send it any message
3. Copy your ID (example: `123456789`)

Option 2 (Via logs):
1. Temporarily add user ID logging to bot code
2. Send /start to your bot
3. Extract ID from logs

### Step 3: Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows PowerShell)
venv\Scripts\Activate.ps1

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Configure Environment

Create `.env` file in project root:

```env
BOT_TOKEN=your_token_from_botfather
ADMIN_CHAT_ID=your_chat_id
TIMEZONE=Europe/Podgorica
```

### Step 5: Run Bot

```bash
python -m app.bot
```

## Project Structure

```
app/
├── bot.py              # Entry point
├── config.py           # Configuration loader
├── db.py               # Database operations
├── states.py           # FSM states definition
├── locales.py          # Translations (3 languages)
├── keyboards.py        # Inline keyboards
├── ai_enhancer.py      # 🤖 AI description enhancement
└── handlers/           # Message handlers
    ├── start.py        # /start and language selection
    ├── lead_flow.py    # Lead collection FSM (with files)
    ├── common.py       # /help, /cancel, /language
    └── my_leads.py     # /my_leads - view and manage leads

scripts/                            # 🔧 Automation scripts
├── backup-bot.sh                   # Automated database backup
├── restore-backup.sh               # Restore from backup
├── check-bot-health.sh             # Health monitoring
├── remote-backup.sh                # Remote backup sync
├── telegram-alert.sh               # Telegram notifications
├── telegram-lead-bot.service       # systemd service template
└── README.md                       # Scripts documentation

requirements.txt                    # Python dependencies
.env                                # Environment variables (not in git)
.env.example                        # Environment variables template
Dockerfile                          # 🐳 Docker image
docker-compose.yml                  # 🐳 Docker Compose config
.dockerignore                       # Docker ignore patterns
leads.db                            # SQLite database (auto-created)
README.md                           # This file
QUICKSTART.md                       # ⚡ Quick start guide
DEPLOYMENT.md                       # 🚀 Production deployment guide
PRODUCTION_CHECKLIST.md             # ✅ Production deployment checklist
CHANGELOG.md                        # 📋 Version history and changes
ROADMAP.md                          # Development roadmap
AI_ENHANCEMENT.md                   # 🤖 AI enhancement documentation
NEW_FEATURES.md                     # 📎 Files + 🔄 Repeat applications
LEAD_MANAGEMENT.md                  # Lead management features
FULL_TEST_CHECKLIST.md              # Complete testing checklist
LANGUAGE_CHANGE_TEST.md             # Language change test results
LANGUAGE_CHANGE_WARNING_TEST.md     # Language change warning tests
```

## Bot Commands

- `/start` - Initial greeting or language selection
- `/new` - Create new lead
- `/my_leads` - View your submitted leads
- `/cancel` - Cancel current form
- `/help` - Show help message
- `/language` - Change interface language

## Database Schema

SQLite database with two tables:

### users
- `tg_user_id` (INTEGER PRIMARY KEY) - Telegram user ID
- `language` (TEXT NOT NULL) - Selected language (ru/me/en)
- `created_at` (TEXT NOT NULL) - Registration timestamp

### leads
- `id` (INTEGER PRIMARY KEY AUTOINCREMENT) - Lead ID
- `tg_user_id` (INTEGER NOT NULL) - User who submitted
- `full_name` (TEXT NOT NULL) - Full name
- `phone` (TEXT NOT NULL) - Phone number
- `email` (TEXT) - Email (optional)
- `description` (TEXT NOT NULL) - Project description
- `files` (TEXT) - JSON array of file IDs (optional)
- `created_at` (TEXT NOT NULL) - Submission timestamp

## Technologies

- Python 3.11+
- aiogram 3.x (Telegram Bot API library)
- SQLite (database)
- python-dotenv (environment management)
- pytz (timezone handling)

## Supported Languages

- Russian (ru)
- Montenegrin (me)
- English (en)

Translations are defined in `app/locales.py`

## Configuration

### Environment Variables

- `BOT_TOKEN` (required) - Telegram bot token from BotFather
- `ADMIN_CHAT_ID` (required) - Telegram chat ID for admin notifications
- `TIMEZONE` (optional) - Timezone for timestamps (default: Europe/Podgorica)
- `DB_PATH` (optional) - SQLite database path (default: leads.db)

## Usage

### Viewing Leads in Database

```bash
sqlite3 leads.db
SELECT * FROM leads;
SELECT * FROM users;
.exit
```

## Troubleshooting

### Bot doesn't respond
- Verify BOT_TOKEN is correct
- Check bot process is running
- Check bot is not blocked in BotFather

### Admin notifications not received
- Verify ADMIN_CHAT_ID is numeric
- Ensure you sent at least one message to bot
- Check logs for errors

### "BOT_TOKEN not found" error
- Verify `.env` file exists in project root
- Check no spaces around `=` in `.env`
- Format: `BOT_TOKEN=123456:ABC` (no quotes)

## Architecture

The bot uses FSM (Finite State Machine) pattern to manage conversation flow. Each user interaction is handled through states that transition based on user input.

Key design principles:
- Dependency injection for database path (testable)
- Type hints on all public functions
- Explicit error handling with specific exceptions
- Input validation at database layer

## Production Deployment

For production deployment on a VPS server:

📖 **[QUICKSTART.md](QUICKSTART.md)** - Step-by-step quick start guide  
📚 **[DEPLOYMENT.md](DEPLOYMENT.md)** - Complete production deployment guide  
✅ **[PRODUCTION_CHECKLIST.md](PRODUCTION_CHECKLIST.md)** - Deployment checklist

### Key Features

- **VPS Setup** - Server configuration and security
- **systemd Service** - Running bot as a system service
- **Docker Deployment** - Containerized deployment option
- **Automated Backups** - Database backup strategies with cron
- **Monitoring** - Logging, alerts, and health checks
- **Security** - Best practices for production environment
- **Updates & Rollback** - Safe update procedures

### Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/telegram-lead-bot.git
cd telegram-lead-bot

# Configure environment
nano .env  # Set BOT_TOKEN and ADMIN_CHAT_ID

# Option 1: Run with systemd
sudo cp scripts/telegram-lead-bot.service /etc/systemd/system/
sudo systemctl start telegram-lead-bot
sudo systemctl enable telegram-lead-bot

# Option 2: Run with Docker
docker compose up -d
```

### Automation Scripts

The `scripts/` directory includes ready-to-use automation tools:

- `backup-bot.sh` - Automated database backup
- `restore-backup.sh` - Restore from backup
- `check-bot-health.sh` - Health monitoring
- `remote-backup.sh` - Sync backups to remote server
- `telegram-alert.sh` - Send alerts via Telegram

See [scripts/README.md](scripts/README.md) for usage details.