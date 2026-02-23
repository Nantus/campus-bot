from enum import Enum
from aiogram.filters import Filter
from aiogram import types


class BotCommands(Enum):
    MyProfile = "👤 Мій профіль" 
    Help = "❓ Допомога"
    Settings = "⚙️ Налаштування"
    AddStatEntry = "Додати запис про зустріч"


class EnumFilter(Filter):
    def __init__(self, command: BotCommands):
        self.command = command

    async def __call__(self, message: types.Message) -> bool:
        return message.text == self.command.value