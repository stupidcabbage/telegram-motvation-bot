import sqlite3 as sl

con = sl.connect('db.sqlite3')

with con:
    con.execute("""
                CREATE TABLE IF NOT EXISTS USER (
                    chat_id INTEGER NOT NULL PRIMARY KEY,
                    username TEXT,
                    is_bot INTEGER
                );
                """)
    con.execute("""
                CREATE TABLE IF NOT EXISTS schedule (
                    chat_id INTEGER NOT NULL,
                    time TEXT,
                    FOREIGN KEY(chat_id) REFERENCES user(chat_id)
                );
                """)