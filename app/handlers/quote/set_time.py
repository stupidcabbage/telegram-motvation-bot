from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from app.handlers.main_handler import send_message
from app.services.validation_time import parse_message, validate_time
from app.states.time import SetTime
from app.templates import render_template
from db.sqlite import check_user_time_in_schedule, create_new_plan_quote


async def set_time_start(message: Message, state: FSMContext) -> None:
    await send_message(
        message.chat.id,
        render_template('set_time.j2'))
    await state.set_state(SetTime.waiting_for_set_time.state)


async def set_time_end(message: Message, state: FSMContext) -> None:
    await state.update_data(time=message.text.lower())
    user_data = await state.get_data()

    if validate_time(user_data.get('time')):

        parsed_message = parse_message(user_data.get('time'))
        if check_user_time_in_schedule(chat_id=message.chat.id,
                                       time=parsed_message):
            await send_message(
                message.chat.id,
                render_template('already_set_time.j2'))
            await state.finish()
        else:
            await send_message(
                chat_id=message.chat.id,
                text=parsed_message)

            create_new_plan_quote(message.chat.id, parsed_message)

            await state.finish()
    else:
        await send_message(
            message.chat.id,
            render_template('error_time.j2', {'delete': False}))
        await state.set_state(SetTime.waiting_for_set_time.state)
