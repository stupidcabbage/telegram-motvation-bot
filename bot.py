import asyncio
import logging

import multiprocessing

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from app.commands import set_commands
from app.services.check_time import check_the_time
from app.handlers.main.register import register_handlers_main
from app.handlers.quote.register import (register_handlers_managment_quote,
                                         register_handlers_quote)
from app.config import TELEGRAM_TOKEN

logger = logging.getLogger(__name__)


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",)

    logger.error('Starting bot')

    bot = Bot(
        token=TELEGRAM_TOKEN,
        parse_mode=types.ParseMode.HTML)
    dp = Dispatcher(bot, storage=MemoryStorage())

    register_handlers_quote(dp)
    register_handlers_main(dp)
    register_handlers_managment_quote(dp)

    await set_commands(bot)

    a = multiprocessing.Process(target=check_the_time)
    a.start()

    await dp.start_polling()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as error:
        logger.critical(f'Бот не смог запустить. Ошибка: {error}')
        raise SystemError('Бот не смог запуститься. Смотрите traceback')
