from aiogram import Dispatcher

from app.handlers.main import help, start


def register_handlers_main(dp: Dispatcher) -> None:
    """Registers the handler for sending the start commands."""
    dp.register_message_handler(start.start, commands=('start'))
    dp.register_message_handler(help.help, commands=('help', 'commands'))
