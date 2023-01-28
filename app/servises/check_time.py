import asyncio
import datetime
import logging
import time

from app.handlers.quote.quote import send_quote_to_person
from db.sqlite import check_time_in_schedule

logger = logging.getLogger(__name__)

CHAT_ID_IN_STASH = 0


def check_time() -> str:
    """Возвращает время форматом hour, minute в словаре."""
    hour = datetime.datetime.now().hour
    minute = datetime.datetime.now().minute
    return parse_time(hour, minute)


def check_the_time() -> None:
    while True:
        try:
            stash = check_time_in_schedule(check_time())
            if len(stash):
                for value in stash:
                    asyncio.run(send_quote_to_person(value[CHAT_ID_IN_STASH]))
        except Exception as error:
            logger.warning(error)
        finally:
            time.sleep(60)


def parse_time(hour: int, minute: int) -> str:
    if hour < 10:
        hour = "0" + str(hour)
    if minute < 10:
        minute = "0" + str(minute)
    return f'{hour}:{minute}'
