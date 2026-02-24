import asyncio
import logging
from aiogram import Bot, Dispatcher

from flows.registration import registragion_router
from flows.add_entry import add_entry_router 

# 1. Налаштування токена та логування
logging.basicConfig(level=logging.INFO)


def get_token() -> str:
    with open("tg_token.txt", "r", encoding="utf-8") as file:
        return file.read().strip()


# Запуск бота
async def main():
    bot = Bot(token=get_token())
    dp = Dispatcher()

    dp.include_router(registragion_router)
    dp.include_router(add_entry_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот вимкнений")