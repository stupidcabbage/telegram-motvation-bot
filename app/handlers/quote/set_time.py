from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from app.handlers.main_handler import send_message
from app.services.validation_time import parse_message, validate_time
from app.states.time import SetTime
from app.texts import ERROR_SET_TIME, HAS_SETTED_TIME, SET_TIME
from db.sqlite import check_user_time_in_schedule, create_new_plan_quote


async def set_time_start(message: Message, state: FSMContext) -> None:
    await send_message(
        message.chat.id,
        SET_TIME)
    await state.set_state(SetTime.waiting_for_set_time.state)


async def set_time_end(message: Message, state: FSMContext) -> None:
    await state.update_data(time=message.text.lower())
    user_data = await state.get_data()

    if validate_time(user_data.get('time')):
        parsed_message = parse_message(user_data.get('time'))
        if check_user_time_in_schedule(message.chat.id, parsed_message):
            await send_message(
                chat_id=message.chat.id,
                text=HAS_SETTED_TIME
            )
            await state.finish()
        else:
            await send_message(
                chat_id=message.chat.id,
                text=parsed_message
                )
            data = {'chat_id': message.chat.id,
                    'time': parsed_message}

            create_new_plan_quote(data)

            await state.finish()
    else:
        await send_message(
            chat_id=message.chat.id,
            text=ERROR_SET_TIME
        )
        await state.set_state(SetTime.waiting_for_set_time.state)
