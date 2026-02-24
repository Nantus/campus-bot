from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
import logging

logger = logging.getLogger("UserActivity")


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: TelegramObject, data):
        if isinstance(event, Message):
            msg : Message = event
            user_id = msg.from_user.id if msg.from_user else "Unknown"
            logger.info(f"User {user_id} sent: {msg.text}")
        return await handler(event, data)