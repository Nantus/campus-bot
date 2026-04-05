from aiogram import Bot, Router, types
from aiogram.fsm.context import FSMContext

from commands import BotCommands, EnumFilter
from database.get_data_from_file import load_admins
from flows.main_menu import enter_main_menu
from flows.settings.admin_settings.admin_settings_keyboard import AdminSettingsKeyboard 

settings_router = Router()


@settings_router.message(EnumFilter(BotCommands.Settings))
async def enter_settings(message: types.Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id if message.from_user else 0

    if str(user_id) in load_admins():
        await message.answer(
            f"Привіт, адмін! У тебе є наступні налаштування:",
            reply_markup=AdminSettingsKeyboard().get_markup(),
        )
    else:
        await enter_main_menu(message=message, state=state, bot=bot)
