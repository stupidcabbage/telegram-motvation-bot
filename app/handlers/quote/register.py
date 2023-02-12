from aiogram import Dispatcher
from app.states.time import DeleteTime, SetTime

from .set_time import set_time_start, set_time_end
from .delete_time import delete_from_schedule, end_delete_from_schedule
from .schedule import check_schedule


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
