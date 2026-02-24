from enum import Enum
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from commands import BotCommands


class NewContactKeyboardReplies(Enum):
    Yes = "Так"
    No = "Ні"


class NewContactKeyboard(ReplyKeyboardBuilder): 
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.button(text=NewContactKeyboardReplies.Yes.value)
        self.button(text=NewContactKeyboardReplies.No.value)
        self.button(text=BotCommands.Cancel.value)
        self.adjust(2) 

    def get_markup(self, resize_keyboard: bool = True, input_field_placeholder: str = "Оберіть пункт меню...") -> ReplyKeyboardMarkup:
        return super().as_markup(resize_keyboard=resize_keyboard, input_field_placeholder=input_field_placeholder)

