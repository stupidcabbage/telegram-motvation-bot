import logging
import re as r
from typing import Match, Optional

from app.services.check_time import parse_time

logger = logging.getLogger(__name__)

VALIDATE_FORM = '^([0-1]?[0-9]|2?[0-3]|[0-9])[:\-\/]([0-5][0-9]|[0-9])$'


def validate_time(time: str) -> Optional[Match[str]]:
    """Validates format time: (M|MM)(:\-/)(H:HH)

    Args:
        time (str): User`s message.

    Returns:
        Optional[Match[str]]: Return all matches or None.
    """
    try:
        logger.debug(f'Validated time: {time}')
        a = r.fullmatch(VALIDATE_FORM, time)
        return a
    except Exception as error:
        logger.error('Time validation error:', error)


def parse_message(time: str) -> str:
    """Returns the parsed message.

    Args:
        time (str): The user`s validated message.

    Returns:
        str: time = HH:MM
    """
    try:
        message = r.split(VALIDATE_FORM, time)
        hour, minute = int(message[1]), int(message[2])
        logger.debug(f'Parsed message with time: {time}')
        return parse_time(hour, minute)
    except Exception as error:
        logger.error('Message parsing error:', error)
