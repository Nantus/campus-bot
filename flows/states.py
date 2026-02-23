from aiogram.fsm.state import State, StatesGroup


class AddStatEntryFlowStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_is_first_pilot = State()
    waiting_for_second_pilot_name = State()
    waiting_for_student_name = State()
    waiting_for_meeting_type = State()
    waiting_for_step_up_number = State()
    waiting_for_meeting_name = State()
    waiting_for_comments = State()