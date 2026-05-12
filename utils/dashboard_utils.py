import re
from datetime import datetime
import mysql.connector
from config import (
    BACKUP_FOLDER,
    LOG_FILE,
    UPLOAD_FOLDER,
    MYSQL_HOST,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_PORT,
)


def formatear_bytes(tamano):
    for unidad in ['B', 'KB', 'MB', 'GB', 'TB']:
        if tamano < 1024:
            return f'{tamano:.1f} {unidad}'
        tamano /= 1024
    return f'{tamano:.1f} PB'


def obtener_estadisticas():
    backup_extensiones = ('.sql', '.gz', '.enc')
    backups = [
        f for f in BACKUP_FOLDER.glob('*')
        if f.is_file() and f.suffix.lower() in backup_extensiones
    ]
    backups.sort(key=lambda item: item.stat().st_mtime)

    total_backups = len(backups)
    total_size = sum(item.stat().st_size for item in backups)
    ultimo_backup = backups[-1] if backups else None

    return {
        'total_backups': total_backups,
        'total_size': formatear_bytes(total_size),
        'ultimo_backup': ultimo_backup.name if ultimo_backup else 'Sin backups',
        'ultimo_backup_fecha': datetime.fromtimestamp(ultimo_backup.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S') if ultimo_backup else 'N/A',
        'ultima_restauracion': obtener_ultima_restauracion(),
        'estado_sistema': obtener_estado_sistema(),
    }


def obtener_ultima_restauracion():
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()

        for linea in reversed(lineas):
            if 'RESTORE' in linea or 'restaurada' in linea.lower():
                match = re.search(r'en ([0-9]+\.[0-9]+)s', linea)
                if match:
                    return f'{match.group(1)} s'
                return linea.strip().split('|')[-1].strip()
    except FileNotFoundError:
        pass

    return 'N/A'


def obtener_estado_sistema():
    estados = []

    try:
        conexion = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port=MYSQL_PORT,
            connection_timeout=5,
        )
        conexion.close()
        estados.append('MySQL conectado')
    except Exception:
        estados.append('Error de conexión MySQL')

    estados.append('Backups disponibles' if BACKUP_FOLDER.exists() else 'Carpeta backups faltante')
    estados.append('Uploads disponibles' if UPLOAD_FOLDER.exists() else 'Carpeta uploads faltante')
    estados.append('Logs disponibles' if LOG_FILE.parent.exists() else 'Carpeta logs faltante')

    return ' · '.join(estados)
