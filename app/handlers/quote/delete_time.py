from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from app.handlers.main_handler import send_message
from app.services.validation_time import parse_message, validate_time
from app.states.time import DeleteTime
from app.texts import (DELETE_QUESTION, ERROR_DELETE_TIME)
from db.sqlite import (check_user_time_in_schedule, delete_all_from_schedule,
                       delete_time_in_schedule)


async def delete_from_schedule(message: Message, state: FSMContext) -> None:
    await send_message(
        message.chat.id,
        DELETE_QUESTION)
    await state.set_state(DeleteTime.waiting_for_get_time)


async def end_delete_from_schedule(message: Message,
                                   state: FSMContext) -> None:

    await state.update_data(time=message.text.lower())
    user_data = (await state.get_data()).get('time')

    if validate_time(user_data):
        parsed_message = parse_message(user_data)

        if check_user_time_in_schedule(message.chat.id, parsed_message):
            await send_message(
                chat_id=message.chat.id,
                text=f'<b>📪 Удалил <i>{parsed_message}</i> из расписания!</b>')

            delete_time_in_schedule(chat_id=message.chat.id,
                                    time=parsed_message)
            await state.finish()
        else:
            await send_message(
                chat_id=message.chat.id,
                text='На это время ничего не назначено!')
            await state.finish()

    elif user_data in ('все', 'всё', 'all'):
        await send_message(
            chat_id=message.chat.id,
            text=f'<b>📪 Удалил <i>{user_data}</i> из расписания!</b>')

        delete_all_from_schedule(message.chat.id)
        await state.finish()

    else:
        await send_message(
            chat_id=message.chat.id,
            text=ERROR_DELETE_TIME)
        await state.set_state(DeleteTime.waiting_for_get_time)
