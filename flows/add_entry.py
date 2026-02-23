from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from chat_states import BotStates
from commands import BotCommands, EnumFilter
from database.write_to_google_sheet import write_to_google_sheet
from flows.states import AddStatEntryFlowStates
from keyboards.is_first_pilot_keyboard import IsFirstPilotKeyboard, IsFirstPilotKeyboardReplies
from keyboards.main_keyboard import MainKeyboard
from keyboards.stepup_number_keyboard import StepUpNumberKeyboard
from keyboards.type_of_meeting_keyboard import TypeOfMeetingKeyboard, TypeOfMeetingKeyboardReplies 

add_entry_router = Router()


@add_entry_router.message(EnumFilter(BotCommands.AddStatEntry))
async def add_stat_entry(message: types.Message, state: FSMContext):
    await message.answer("Давай додамо новий запис про зустріч.")
    await message.answer(
        "Як тебе звати?",
        reply_markup=ReplyKeyboardRemove(),
    )

    await state.set_state(AddStatEntryFlowStates.waiting_for_name)


@add_entry_router.message(AddStatEntryFlowStates.waiting_for_name)
async def enter_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(
        "Чи був ти першим пілотом на цій зустрічі?",
        reply_markup=IsFirstPilotKeyboard().get_markup(),
    )

    await state.set_state(AddStatEntryFlowStates.waiting_for_is_first_pilot)


@add_entry_router.message(AddStatEntryFlowStates.waiting_for_is_first_pilot)
async def is_first_pilot(message: types.Message, state: FSMContext):
    if message.text == IsFirstPilotKeyboardReplies.No.value:
        await message.answer("Попроси, будь ласка, першого пілота занести інформацію про цю зустріч.")
        await message.answer(
            "Па-па!",
            reply_markup=MainKeyboard().get_markup(),
        )
        await state.set_state(BotStates.waiting_for_entry)
        return
    elif message.text == IsFirstPilotKeyboardReplies.Yes.value: 
        await message.answer(
            "Хто був твоїм другим пілотом? Напиши ім'я",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.set_state(AddStatEntryFlowStates.waiting_for_second_pilot_name)


@add_entry_router.message(AddStatEntryFlowStates.waiting_for_second_pilot_name)
async def second_pilot_name(message: types.Message, state: FSMContext):
    await state.update_data(second_pilon_name=message.text)
    await message.answer(
        "Для кого ти проводив цю зустріч? Напиши ім'я студента",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(AddStatEntryFlowStates.waiting_for_student_name)


@add_entry_router.message(AddStatEntryFlowStates.waiting_for_student_name)
async def student_name(message: types.Message, state: FSMContext):
    await state.update_data(student_name=message.text)
    await message.answer(
        "Тепер обери, що це була за зустріч?",
        reply_markup=TypeOfMeetingKeyboard().get_markup(),
    )
    await state.set_state(AddStatEntryFlowStates.waiting_for_meeting_type)


@add_entry_router.message(AddStatEntryFlowStates.waiting_for_meeting_type)
async def meeting_type(message: types.Message, state: FSMContext):
    if message.text in (TypeOfMeetingKeyboardReplies.Worldview.value, TypeOfMeetingKeyboardReplies.Photoquest.value):
        await state.update_data(meeting_type=message.text)
        await state.update_data(step_up_number="0")
        await message.answer("Можливо, у тебе є якісь коментарі до цієї зустрічі?")
        await state.set_state(AddStatEntryFlowStates.waiting_for_comments)
        return
    elif message.text == TypeOfMeetingKeyboardReplies.Stepup.value: 
        await message.answer(
            "Обери номер степапу",
            reply_markup=StepUpNumberKeyboard().get_markup(),
        )
        await state.set_state(AddStatEntryFlowStates.waiting_for_step_up_number)
    else: 
        await message.answer(
            "Напиши, що це була за зустріч.",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.set_state(AddStatEntryFlowStates.waiting_for_meeting_name)


@add_entry_router.message(AddStatEntryFlowStates.waiting_for_meeting_name)
async def meeting_name(message: types.Message, state: FSMContext):
    await state.update_data(meeting_type=message.text)
    await state.update_data(step_up_number="0")
    await message.answer(
        "Можливо, у тебе є якісь коментарі до цієї зустрічі?",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(AddStatEntryFlowStates.waiting_for_comments)


@add_entry_router.message(AddStatEntryFlowStates.waiting_for_step_up_number)
async def step_up_number(message: types.Message, state: FSMContext):
    await state.update_data(meeting_type=TypeOfMeetingKeyboardReplies.Stepup.value)
    await state.update_data(step_up_number=message.text)
    await message.answer(
        "Можливо, у тебе є якісь коментарі до цієї зустрічі?",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(AddStatEntryFlowStates.waiting_for_comments)


@add_entry_router.message(AddStatEntryFlowStates.waiting_for_comments)
async def comments(message: types.Message, state: FSMContext):
    await state.update_data(comments=message.text)
    data = await state.get_data() 
    write_to_google_sheet(list(data.values()))
    await message.answer(
        "Зустріч записано. Дякую за твоє служіння!",
        reply_markup=MainKeyboard().get_markup(),
    )
    await state.clear()
    await state.set_state(BotStates.waiting_for_entry)