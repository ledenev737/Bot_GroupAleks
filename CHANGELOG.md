# Changelog

Все значимые изменения в этом проекте документируются в этом файле.

Формат основан на [Keep a Changelog](https://keepachangelog.com/ru/1.0.0/),
и этот проект следует [Semantic Versioning](https://semver.org/lang/ru/).

## [Unreleased]

### Added
- 🚀 Production deployment documentation
  - Comprehensive DEPLOYMENT.md guide
  - Quick start guide (QUICKSTART.md)
  - Docker support (Dockerfile, docker-compose.yml)
  - systemd service template
- 🔧 Automation scripts for production:
  - Automated backup script (backup-bot.sh)
  - Backup restore script (restore-backup.sh)
  - Health check monitoring (check-bot-health.sh)
  - Remote backup sync (remote-backup.sh)
  - Telegram alerts (telegram-alert.sh)
- 📝 Scripts documentation (scripts/README.md)

### Changed
- Updated README.md with production deployment section
- Enhanced .gitignore with backup and Docker entries
- Updated project structure documentation

## [1.2.0] - 2025-01-XX

### Added
- 📎 File attachments support (photos, documents, videos)
- 🔄 Smart repeat applications with contact data reuse
- 🤖 AI-powered description enhancement
- Lead management features:
  - View submitted leads with /my_leads
  - Edit existing leads
  - Delete leads
  - Detailed lead viewing

### Changed
- Improved user experience with repeat submissions
- Enhanced FSM flow for file handling

### Documentation
- NEW_FEATURES.md - File attachments and repeat applications
- LEAD_MANAGEMENT.md - Lead management documentation
- AI_ENHANCEMENT.md - AI enhancement features
- FULL_TEST_CHECKLIST.md - Complete testing checklist
- LANGUAGE_CHANGE_TEST.md - Language change tests

## [1.1.0] - 2024-XX-XX

### Added
- Multi-language support (Russian, Montenegrin, English)
- Language selection and switching
- Admin notifications with detailed lead info

### Changed
- Improved keyboard layouts
- Enhanced error handling

## [1.0.0] - 2024-XX-XX

### Added
- Initial release
- Basic lead collection form
- SQLite database storage
- FSM-based conversation flow
- Phone and email validation
- /start, /help, /cancel commands

---

## Типы изменений

- **Added** - новые функции
- **Changed** - изменения в существующей функциональности
- **Deprecated** - функции, которые скоро будут удалены
- **Removed** - удалённые функции
- **Fixed** - исправления багов
- **Security** - исправления уязвимостей
- **Documentation** - изменения в документации

---

## Планы на будущее

См. [ROADMAP.md](ROADMAP.md) для подробного плана развития проекта.

### Ближайшие планы

- [ ] Добавить поддержку webhook (для production)
- [ ] Интеграция с CRM системами
- [ ] Экспорт заявок в различные форматы
- [ ] Web-интерфейс для управления заявками
- [ ] Расширенная аналитика и статистика
- [ ] Настраиваемые поля формы
- [ ] Шаблоны уведомлений

---

## Как внести изменения

Если вы хотите внести свой вклад в проект:

1. Форкните репозиторий
2. Создайте ветку для вашей функции (`git checkout -b feature/AmazingFeature`)
3. Закоммитьте изменения (`git commit -m 'Add some AmazingFeature'`)
4. Запушьте в ветку (`git push origin feature/AmazingFeature`)
5. Откройте Pull Request

При добавлении изменений не забудьте обновить этот CHANGELOG.md!

---

## Версионирование

Мы используем [SemVer](http://semver.org/) для версионирования. Доступные версии смотрите в [releases](https://github.com/yourusername/telegram-lead-bot/releases).

**Формат версии: MAJOR.MINOR.PATCH**

- **MAJOR** - несовместимые изменения API
- **MINOR** - новая функциональность с обратной совместимостью
- **PATCH** - исправления багов с обратной совместимостью
