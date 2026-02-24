from aiogram import Bot, Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from chat_states import BotStates
from flows.main_menu import enter_main_menu
from keyboards.main_keyboard import MainKeyboard 
from database.database import db

registragion_router = Router()


@registragion_router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext, bot: Bot):
    stored_name = db.get_name(message.from_user.id if message.from_user else 0)

    if stored_name:
        await message.answer(f"Привіт знову, {stored_name}! Чим допомогти?")
        await enter_main_menu(message=message, state=state, bot=bot)
    else:
        await message.answer("Привіт! Я твій бот. Як мені до тебе звертатися?")
        await state.set_state(BotStates.waiting_for_name)


@registragion_router.message(BotStates.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext, bot: Bot):
    user_name = message.text
    user_id = message.from_user.id if message.from_user else 0

    db.set_name(user_id, user_name)
    await state.update_data(name=user_name)
    
    await message.answer(
        f"Приємно познайомитись, {user_name}!",
    )
    await enter_main_menu(message=message, state=state, bot=bot)
