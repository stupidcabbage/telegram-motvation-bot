from typing import Optional
import logging

import sqlite3 as sl


con = sl.connect('first.db')

logger = logging.getLogger(__name__)


def create_new_user(username: str, chat_id: int, is_bot: int) -> None:
    """Create new user in DB.

    Args:
        chat_id: int,
        username: str,
        is_bot: int.
    """
    with con:
        con.execute(f'INSERT INTO user (chat_id, username, is_bot) \
                    VALUES({chat_id}, "{username}", {is_bot});')


def check_user(chat_id: int) -> Optional[tuple]:
    """Checks the presence of the user in the database.

    Args:
        data (dict):
            chat_id: int,

    Returns:
        Optional[tuple]:
            chat_id: int,
            username: str,
            is_bot: int.
    """
    sql = f'SELECT * FROM USER WHERE (chat_id={chat_id})'
    return _get_request(sql)


def create_new_plan_quote(chat_id: int, time: str) -> None:
    with con:
        con.execute(f'INSERT INTO schedule (chat_id, time) \
                    VALUES({chat_id}, "{time}")')


def check_time_in_schedule(time: str) -> Optional[tuple]:
    sql = f'SELECT * FROM schedule WHERE (time="{time}")'
    return _get_request(sql)


def check_user_schedule(chat_id: int) -> Optional[tuple]:
    sql = f'SELECT * FROM schedule WHERE (chat_id={chat_id})'
    return _get_request(sql)


def check_user_time_in_schedule(chat_id: int, time: str) -> Optional[tuple]:
    sql = f'SELECT * FROM schedule WHERE (chat_id={chat_id} AND time="{time}")'
    return _get_request(sql)


def delete_time_in_schedule(chat_id: int, time: str):
    sql = f'DELETE FROM schedule WHERE chat_id={chat_id} AND time="{time}";'
    with con:
        con.execute(sql)


def delete_all_from_schedule(chat_id: int):
    sql = f'DELETE FROM schedule where chat_id={chat_id}'
    with con:
        con.execute(sql)


def _get_request(sql):
    with con:
        request = con.execute(sql)
        a = []
        for i in request:
            a.append(i)
        return a
