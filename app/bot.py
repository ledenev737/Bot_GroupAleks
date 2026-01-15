"""
Точка входа - запуск Telegram бота
"""
import asyncio
import logging
import sys
import os

# Устанавливаем кодировку UTF-8 для Windows консоли
if sys.platform == 'win32':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.config import BOT_TOKEN, DB_PATH
from app.db import init_db
from app.handlers import start, lead_flow, common, my_leads

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)


async def main():
    """
    Главная функция - инициализация и запуск бота
    """
    # Инициализируем базу данных
    init_db(DB_PATH)
    
    # Создаем бота
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    # Создаем диспетчер
    dp = Dispatcher()
    
    # Регистрируем роутеры (порядок важен!)
    dp.include_router(start.router)
    dp.include_router(common.router)
    dp.include_router(my_leads.router)
    dp.include_router(lead_flow.router)
    
    logger.info("🚀 Бот запущен и готов к работе!")
    
    # Запускаем polling (long polling)
    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⛔ Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
        raise
