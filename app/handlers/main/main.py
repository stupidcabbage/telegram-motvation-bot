import logging

from aiogram import Dispatcher
from aiogram.types import Message

from app.handlers.main_handler import send_message
from app.texts import HELP, make_start_text
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
    await send_message(chat_id=message.chat.id,
                       text=await make_start_text(message.chat.first_name))


async def send_commands_message(message: Message) -> None:
    """Sends help message.

    Args:
        message (Message): User telegram message.`
    """
    await send_message(chat_id=message.chat.id,
                       text=HELP)


def register_handlers_main(dp: Dispatcher) -> None:
    """Registers the handler for sending the start commands."""
    dp.register_message_handler(send_first_message, commands=('start'))
    dp.register_message_handler(send_commands_message, commands=('help',
                                                                 'commands'))
