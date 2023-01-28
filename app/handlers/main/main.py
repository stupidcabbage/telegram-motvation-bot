import logging

from aiogram import Dispatcher
from aiogram.types import Message

from app.handlers.main_handler import send_message
from db.sqlite import check_user, create_new_user

logger = logging.getLogger(__name__)


async def send_first_message(message: Message) -> None:
    """Sends the first message and adds the user to the DB.

    Args:
        message (Message): telegram message by user.`
    """
    if not check_user({'chat_id': message.chat.id}):
        data = {
            'chat_id': message.chat.id,
            'username': message.chat.username,
            'is_bot': 0
        }
        create_new_user(data)
    await send_message(chat_id=message.chat.id,
                       text=f'Привет, {message.chat.first_name}')


def register_handlers_main(dp: Dispatcher) -> None:
    """Регистрирует обработчик отправки стартовых команд."""
    dp.register_message_handler(send_first_message, commands=('start', 'help'))
