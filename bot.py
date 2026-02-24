import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram_sqlite_storage.sqlitestore import SQLStorage

from flows.registration import registragion_router
from flows.cancel import cancel_router 
from flows.add_new_entry.add_entry import add_entry_router
from flows.give_a_new_contact.give_a_new_contact import give_a_new_contact_router 
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
    storage = SQLStorage("fsm_states.db")
    dp = Dispatcher(storage=storage)

    dp.message.middleware(LoggingMiddleware())
    dp.include_router(cancel_router)
    dp.include_router(registragion_router)
    dp.include_router(add_entry_router)
    dp.include_router(give_a_new_contact_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот вимкнений")