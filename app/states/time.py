from aiogram.dispatcher.filters.state import State, StatesGroup


class SetTime(StatesGroup):
    waiting_for_set_time = State()


class DeleteTime(StatesGroup):
    waiting_for_get_time = State()
