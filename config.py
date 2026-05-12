import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')


def _env_int(name, default):
    try:
        return int(os.getenv(name, default))
    except (TypeError, ValueError):
        return default


BACKUP_FOLDER = Path(os.getenv('BACKUP_FOLDER', BASE_DIR / 'backups'))
UPLOAD_FOLDER = Path(os.getenv('UPLOAD_FOLDER', BASE_DIR / 'uploads'))
LOG_FILE = Path(os.getenv('LOG_FILE', BASE_DIR / 'logs' / 'logs.txt'))
MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
MYSQL_PORT = _env_int('MYSQL_PORT', 3306)
MYSQL_PATH = os.getenv(
    'MYSQL_PATH',
    str(BASE_DIR / 'mysql' / 'bin' / 'mysql.exe')
)
MYSQLDUMP_PATH = os.getenv(
    'MYSQLDUMP_PATH',
    str(Path(MYSQL_PATH).with_name('mysqldump.exe'))
)
FLASK_SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'change-this-secret')
ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'admin')
AUTO_BACKUP_INTERVAL_MINUTES = _env_int('AUTO_BACKUP_INTERVAL_MINUTES', 0)

for folder in (BACKUP_FOLDER, UPLOAD_FOLDER, LOG_FILE.parent):
    folder.mkdir(parents=True, exist_ok=True)
