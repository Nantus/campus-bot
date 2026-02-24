import asyncio
import logging
from aiogram import Bot, Dispatcher

from flows.registration import registragion_router
from flows.add_entry import add_entry_router
from logger.middlewares_logging import LoggingMiddleware 
from logging.handlers import RotatingFileHandler

log_format = '%(asctime)s - %(levelname)s - %(name)s - %(message)s'

logging.basicConfig(
    level=logging.INFO, 
    format=log_format,
    handlers=[
        RotatingFileHandler(
            "./logs/bot_log.log", 
            maxBytes=5000000, 
            backupCount=5,
            encoding="utf-8",
        ),
        logging.StreamHandler()
    ]
)

logging.basicConfig(level=logging.INFO)


def get_token() -> str:
    with open("tg_token.txt", "r", encoding="utf-8") as file:
        return file.read().strip()


async def main():
    bot = Bot(token=get_token())
    dp = Dispatcher()

    dp.message.middleware(LoggingMiddleware())
    dp.include_router(registragion_router)
    dp.include_router(add_entry_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот вимкнений")