import logging

from aiogram import Dispatcher
from aiogram.types import Message

from app.templates import render_template
from app.handlers.main_handler import send_message
from db.sqlite import check_user, create_new_user

logger = logging.getLogger(__name__)


async def send_first_message(message: Message) -> None:
    """Sends the first message and adds the user to the DB.

    Args:
        message (Message): User telegram message`
    """
    if not check_user(message.chat.id):
        create_new_user(chat_id=message.chat.id,
                        username=message.chat.username,
                        is_bot=0)
    await send_message(message.chat.id,
                       render_template(
                           'start.j2',
                           {'first_name': message.chat.first_name}))


async def send_commands_message(message: Message) -> None:
    """Sends help message.

    Args:
        message (Message): User telegram message.`
    """
    await send_message(chat_id=message.chat.id,
                       text=render_template('help.j2'))


def register_handlers_main(dp: Dispatcher) -> None:
    """Registers the handler for sending the start commands."""
    dp.register_message_handler(send_first_message, commands=('start'))
    dp.register_message_handler(send_commands_message, commands=('help',
                                                                 'commands'))
