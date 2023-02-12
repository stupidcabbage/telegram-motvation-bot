from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from app.templates import render_template

from app.handlers.main_handler import send_message
from app.services.validation_time import parse_message, validate_time
from app.states.time import DeleteTime
from db.sqlite import (check_user_time_in_schedule, delete_all_from_schedule,
                       delete_time_in_schedule)


async def delete_from_schedule(message: Message, state: FSMContext) -> None:
    await send_message(
        message.chat.id,
        render_template('delete_time.j2'))
    await state.set_state(DeleteTime.waiting_for_get_time)


async def end_delete_from_schedule(message: Message,
                                   state: FSMContext) -> None:

    await state.update_data(time=message.text.lower())
    user_data = (await state.get_data()).get('time')

    if validate_time(user_data):
        parsed_message = parse_message(user_data)

        if check_user_time_in_schedule(message.chat.id, parsed_message):
            await send_message(
                message.chat.id,
                render_template('already_delete_time.j2',
                                {'time': parsed_message}))

            delete_time_in_schedule(chat_id=message.chat.id,
                                    time=parsed_message)
            await state.finish()
        else:
            await send_message(
                message.chat.id,
                render_template('already_delete_time.j2'))
            await state.finish()

    elif user_data in ('все', 'всё', 'all'):
        await send_message(
            message.chat.id,
            render_template('already_delete_time.j2',
                            {'time': user_data}))

        delete_all_from_schedule(message.chat.id)
        await state.finish()

    else:
        await send_message(
            message.chat.id,
            render_template('error_time.j2', {'delete': True}))
        await state.set_state(DeleteTime.waiting_for_get_time)
