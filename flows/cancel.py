from aiogram import Bot, Router, types
from aiogram.fsm.context import FSMContext

from commands import BotCommands, EnumFilter
from flows.main_menu import enter_main_menu

cancel_router = Router()


@cancel_router.message(EnumFilter(BotCommands.Cancel))
async def cancel(message: types.Message, state: FSMContext, bot: Bot):
    await message.answer("Скасовуємо процесс...")
    await state.clear()
    await enter_main_menu(message=message, state=state, bot=bot)
    