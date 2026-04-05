from aiogram.fsm.state import State, StatesGroup


class BroadcastToAllStates(StatesGroup):
    waiting_for_message_to_all = State()