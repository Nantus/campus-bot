from aiogram import BaseMiddleware
from aiogram.types import Message
import logging

logger = logging.getLogger("UserActivity")


class LoggingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        logger.info(f"User {event.from_user.id} sent: {event.text}")
        return await handler(event, data)