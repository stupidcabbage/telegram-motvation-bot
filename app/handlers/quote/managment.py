import logging

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from app.states.time import SetTime, DeleteTime
from app.texts import (SET_TIME, HAS_SETTED_TIME, ERROR_SET_TIME,
                       ERROR_DELETE_TIME, DELETE_QUESTION)
from app.handlers.main_handler import send_message
from app.services.validation_time import parse_message, validate_time
from db.sqlite import (check_user_schedule, create_new_plan_quote,
                       delete_time_in_schedule, delete_all_from_schedule,
                       check_user_time_in_schedule)

logger = logging.getLogger(__name__)


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


async def check_schedule(message: Message) -> None:
    schedule_time = check_user_schedule(message.chat.id)
    await send_message(chat_id=message.chat.id, text=schedule_time)


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


def register_handlers_managment_quote(dp: Dispatcher) -> None:
    """Регистрирует обработчик создания и изменения времени для отправки."""
    dp.register_message_handler(set_time_start,
                                commands='set_time',
                                state='*')
    dp.register_message_handler(check_schedule,
                                commands='schedule')
    dp.register_message_handler(set_time_end,
                                state=SetTime.waiting_for_set_time)
    dp.register_message_handler(delete_from_schedule,
                                commands='delete_time',
                                state='*')
    dp.register_message_handler(end_delete_from_schedule,
                                state=DeleteTime.waiting_for_get_time)
