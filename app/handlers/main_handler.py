import logging
from typing import Union

from aiogram import Bot, types

from config.config_reader import load_config

logger = logging.getLogger(__name__)

config = load_config('config/bot.ini')

bot = Bot(
    token=config.tg_bot.token,
    parse_mode=types.ParseMode.HTML)


async def send_message(chat_id: Union[str, int], text: str) -> None:
    """Send message to user.

    Args:
        chat_id (Union[str, int]): User chat ID
        text (str): Message text
    """
    try:
        logger.info(f'Send message to {chat_id}. Text: {text}')
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception as error:
        logger.critical(f'Error with sending message. {error}')
