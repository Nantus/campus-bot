import asyncio
import logging

from aiogram import Bot, Router, types
from aiogram.fsm.context import FSMContext

from commands import EnumFilter
from database.get_data_from_file import load_admins
from flows.main_menu import enter_main_menu
from flows.settings.admin_settings.admin_settings_keyboard import AdminSettingsKeyboardReplies
from flows.settings.admin_settings.broadcast_to_all.states import BroadcastToAllStates
from keyboards.cancel_keyboard import CancelKeyboard
from database.database import db

broadcast_to_all_router = Router()


@broadcast_to_all_router.message(EnumFilter(AdminSettingsKeyboardReplies.BroadcastToAll))
async def broadcast_to_all(message: types.Message, state: FSMContext, bot: Bot):
    user_id = message.from_user.id if message.from_user else 0

    if str(user_id) not in load_admins():
        await enter_main_menu(message=message, state=state, bot=bot)

    await message.answer(
        f"Яке повідомлення ти хочеш всім надіслати?",
        reply_markup=CancelKeyboard().get_markup(),
    )
    await state.set_state(BroadcastToAllStates.waiting_for_message_to_all)


@broadcast_to_all_router.message(BroadcastToAllStates.waiting_for_message_to_all)
async def send_message_to_all(message: types.Message, state: FSMContext, bot: Bot):
    users = db.get_all_users()
    broadcast_message = message.text or ""
    count = 0
    blocked_count = 0

    if not broadcast_message:
        await enter_main_menu(message, state, bot)

    await message.answer(f"🚀 Починаю розсилку на {len(users)} користувачів...")
    for user_id in users:
        try:
            await bot.send_message(user_id, broadcast_message)
            count += 1
            await asyncio.sleep(0.05) 
        except Exception as e:
            blocked_count += 1
            logging.error(f"Помилка при надсиланні {user_id}: {e}")
    
    await message.answer(f"✅ Розсилка завершена!\n\n📈 Отримали: {count}\n🚫 Заблокували бота: {blocked_count}")
    await enter_main_menu(message, state, bot)
