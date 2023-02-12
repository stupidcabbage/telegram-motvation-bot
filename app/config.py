import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN', '')

BASEDIR = Path(__file__).resolve().parent
TEMPLATES_DIR = BASEDIR / 'templates'
SQL_LITE_DB_FILE = BASEDIR / 'db.sqlite3'
