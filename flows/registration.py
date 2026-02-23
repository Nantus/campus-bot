from aiogram import Router, types
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from chat_states import BotStates
from keyboards.main_keyboard import MainKeyboard 

registragion_router = Router()


# @registragion_router.message(CommandStart())
# async def cmd_start(message: types.Message, state: FSMContext):
#     # Перевіряємо, чи ми вже знаємо ім'я (в реальних проектах тут запит до БД)
#     user_data = await state.get_data()
    
#     if "name" in user_data:
#         await message.answer(f"Привіт знову, {user_data['name']}! Чим допомогти?")
#     else:
#         await message.answer("Привіт! Я твій бот. Як мені до тебе звертатися?")
#         # Переводимо користувача у стан очікування імені
#         await state.set_state(BotStates.waiting_for_name)


@registragion_router.message(BotStates.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    
    # Надсилаємо повідомлення разом із кнопками
    await message.answer(
        f"Приємно познайомитись, {message.text}! Тепер у тебе є меню:",
        reply_markup=MainKeyboard().get_markup(),
    )
    
    await state.set_state(BotStates.waiting_for_entry)


@registragion_router.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    await message.answer(
        f"Привіт! У тебе є меню:",
        reply_markup=MainKeyboard().get_markup(),
    )
    
    await state.set_state(BotStates.waiting_for_entry)