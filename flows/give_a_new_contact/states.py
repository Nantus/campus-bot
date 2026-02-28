from aiogram.fsm.state import State, StatesGroup


class GiveANewContactStates(StatesGroup):
    waiting_for_acception_reply = State()
