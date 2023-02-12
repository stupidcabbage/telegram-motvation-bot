import logging

from aiogram.types import Message

from app.handlers.main_handler import send_message
from app.templates import render_template
from db.sqlite import check_user, create_new_user

logger = logging.getLogger(__name__)


async def start(message: Message) -> None:
    """Sends the first message and adds the user to the DB."""
    if not check_user(message.chat.id):
        create_new_user(chat_id=message.chat.id,
                        username=message.chat.username,
                        is_bot=0)
    await send_message(
        message.chat.id,
        render_template('start.j2',
                        {'first_name': message.chat.first_name}))
