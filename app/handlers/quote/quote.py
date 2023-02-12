import logging
from typing import Union

from aiogram import Dispatcher
from aiogram.types import Message

from app.handlers.main_handler import send_message
from app.services.get_quote import get_quote, get_reserve_quote

logger = logging.getLogger(__name__)


async def send_quote_to_person(chat_id: int) -> None:
    """Запрашивает и отправляет цитату на руссском языке,
    иначе на английском определенному человеку."""
    try:
        answer = await get_quote()
        logger.info(f'Send plan quote - {chat_id}')
        await send_quote_message(chat_id=chat_id, answer=answer)
    except Exception as error:
        logger.error(f'Error in sening a planned quote to {chat_id}: {error}')
        answer = await get_reserve_quote()
        await send_quote_message(chat_id=chat_id, answer=answer)


async def send_quote(message: Message) -> None:
    """Запрашивает и отправляет цитату на русском языке, иначе на английском"""
    try:
        answer = await get_quote()
        logger.info(f'Send quote - {message.chat.id}: {message.chat.username}')
        await send_quote_message(message.chat.id, answer)
    except Exception as error:
        logger.error(f'Error in sening a planned quote: {error}')
        answer = await get_reserve_quote()
        await send_quote_message(message.chat.id, answer)


async def send_quote_message(chat_id: Union[str, int],
                             answer: dict[str, str]) -> None:
    """Отправляет цитату, следуя стандарту:
    <BOLD BODY> <пропуск в две строки> <AUTHOR>."""
    text = await parse_message(answer=answer)
    await send_message(chat_id=chat_id, text=text)


async def parse_message(answer: dict[str, str]) -> str:
    """Парсит и формирует сообщение."""
    return f"<b>{answer.get('text')}</b> \n\n{answer.get('author')}"


def register_handlers_quote(dp: Dispatcher) -> None:
    """Регистрирует обработчик отправки высказываний"""
    dp.register_message_handler(send_quote, commands='quote')
