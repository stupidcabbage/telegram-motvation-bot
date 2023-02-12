import logging

from aiogram.types import Message

from app.handlers.main_handler import send_message
from db.sqlite import check_user_schedule

logger = logging.getLogger(__name__)


async def check_schedule(message: Message) -> None:
    schedule_time = check_user_schedule(chat_id=message.chat.id)
    await send_message(chat_id=message.chat.id, text=schedule_time)
