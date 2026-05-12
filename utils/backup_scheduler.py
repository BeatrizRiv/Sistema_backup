from threading import Timer
from config import AUTO_BACKUP_INTERVAL_MINUTES, MYSQL_PASSWORD
from utils.backup_utils import crear_backup_automatico
from utils.log_utils import guardar_log


def _programar_backup():
    resultado, detalles = crear_backup_automatico(MYSQL_PASSWORD)
    guardar_log(f'{resultado} | {"; ".join(detalles)}')
    Timer(AUTO_BACKUP_INTERVAL_MINUTES * 60, _programar_backup).start()


def iniciar_backup_automatico():
    if AUTO_BACKUP_INTERVAL_MINUTES and AUTO_BACKUP_INTERVAL_MINUTES > 0:
        Timer(AUTO_BACKUP_INTERVAL_MINUTES * 60, _programar_backup).start()
