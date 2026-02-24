from aiogram import Bot, types
from aiogram.fsm.context import FSMContext

from chat_states import BotStates
from keyboards.main_keyboard import MainKeyboard


async def enter_main_menu(message: types.Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id if message.from_user else 0 
    await bot.send_message(
        chat_id=user_id,
        text=f"У тебе є меню:",
        reply_markup=MainKeyboard().get_markup(),
    )
    
    await state.set_state(BotStates.waiting_for_entry)
