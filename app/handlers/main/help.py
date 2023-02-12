import logging

from aiogram.types import Message

from app.templates import render_template
from app.handlers.main_handler import send_message

logger = logging.getLogger(__name__)


async def help(message: Message) -> None:
    """Sends help message.

    Args:
        message (Message): User telegram message.`
    """
    await send_message(chat_id=message.chat.id,
                       text=render_template('help.j2'))
