from aiogram import Bot, Router, types
from aiogram.fsm.context import FSMContext

from commands import BotCommands, EnumFilter
from database.write_to_google_sheet import read_from_google_sheet, write_one_cell
from flows.give_a_new_contact.filter_data_frame import filter_data_frame
from flows.give_a_new_contact.new_contact_keyboard import NewContactKeyboard, NewContactKeyboardReplies
from flows.give_a_new_contact.states import GiveANewContactStates
from database.database import db
from flows.main_menu import enter_main_menu

give_a_new_contact_router = Router()


@give_a_new_contact_router.message(EnumFilter(BotCommands.GiveANewContact))
async def give_a_new_contact(message: types.Message, state: FSMContext, bot: Bot):
    await message.answer("Секунуду, шукаю тобі людину серед реєстрацій...")
    df = read_from_google_sheet()
    if new_contact := filter_data_frame(df):
        await state.update_data(row_number=new_contact.row_number)
        await message.answer("Знайшовся контакт!")
        await message.answer(f"Ім'я: {new_contact.name} \nТелеграм: {new_contact.telegram} \nКурс: {new_contact.grade} \nКоментарі: {new_contact.comments}")
        await message.answer(
            "Береш?",
            reply_markup=NewContactKeyboard().get_markup(),
        )
        await state.set_state(GiveANewContactStates.waiting_for_acception_reply)
    else: 
        await message.answer("Схоже, що зараз всіх людей вже розібрали...")
        await enter_main_menu(message, state, bot)


@give_a_new_contact_router.message(GiveANewContactStates.waiting_for_acception_reply)
async def acception_reply(message: types.Message, state: FSMContext, bot: Bot):
    if message.text == NewContactKeyboardReplies.Yes.value:
        await message.answer("Чудово! Я запишу в таблицю, що тепер ця людина буде проходити зустрічі з тобою!")
        data = await state.get_data()
        if row_number := data.get("row_number"):
            write_one_cell("D", row_number, db.get_name(message.from_user.id if message.from_user else 0))
    elif message.text == NewContactKeyboardReplies.No.value:
        await state.clear()
    await enter_main_menu(message, state, bot)