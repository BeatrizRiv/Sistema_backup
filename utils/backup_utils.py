import gzip
import mysql.connector
import subprocess
from datetime import datetime
from pathlib import Path
from utils.crypto_utils import fernet
from config import (
    BACKUP_FOLDER,
    MYSQL_HOST,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_PORT,
    MYSQLDUMP_PATH,
)


def crear_backup(database, tipo, password):
    try:
        conexion = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=password,
            port=MYSQL_PORT,
        )

        cursor = conexion.cursor()
        cursor.execute('SHOW DATABASES')
        bases = [db[0] for db in cursor]
        conexion.close()

        if database not in bases:
            return '❌ La base de datos no existe', None

        fecha = datetime.now().strftime('%Y%m%d_%H%M%S')
        sql_file = BACKUP_FOLDER / f'{database}_{fecha}.sql'

        comando = (
            f'"{MYSQLDUMP_PATH}" -u "{MYSQL_USER}" -p"{password}" '
            f'-h "{MYSQL_HOST}" -P "{MYSQL_PORT}" "{database}" > "{sql_file}"'
        )
        subprocess.run(comando, shell=True, check=False)

        if tipo == 'sql':
            return '✅ Backup SQL creado correctamente', str(sql_file)

        elif tipo == 'gz':
            gz_file = Path(f'{sql_file}.gz')
            with open(sql_file, 'rb') as f_in:
                with gzip.open(gz_file, 'wb') as f_out:
                    f_out.writelines(f_in)
            sql_file.unlink(missing_ok=True)
            return '✅ Backup comprimido creado correctamente', str(gz_file)

        elif tipo == 'enc':
            gz_file = Path(f'{sql_file}.gz')
            with open(sql_file, 'rb') as f_in:
                with gzip.open(gz_file, 'wb') as f_out:
                    f_out.writelines(f_in)

            with open(gz_file, 'rb') as archivo:
                datos = archivo.read()

            datos_cifrados = fernet.encrypt(datos)
            enc_file = BACKUP_FOLDER / f'{database}_{fecha}.enc'
            with open(enc_file, 'wb') as archivo:
                archivo.write(datos_cifrados)

            sql_file.unlink(missing_ok=True)
            gz_file.unlink(missing_ok=True)
            return '✅ Backup cifrado creado correctamente', str(enc_file)

        return '❌ Tipo de backup no reconocido', None

    except Exception as e:
        return f'❌ Error: {str(e)}', None


def crear_backup_automatico(password):
    try:
        conexion = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=password,
            port=MYSQL_PORT,
        )

        cursor = conexion.cursor()
        cursor.execute('SHOW DATABASES')
        bases = [db[0] for db in cursor if db[0] not in (
            'information_schema',
            'mysql',
            'performance_schema',
            'sys',
        )]
        conexion.close()

        if not bases:
            return '❌ No hay bases válidas para backup automático', []

        fecha = datetime.now().strftime('%Y%m%d_%H%M%S')
        detalles = []

        for database in bases:
            sql_file = BACKUP_FOLDER / f'{database}_{fecha}.sql'
            comando = (
                f'"{MYSQLDUMP_PATH}" -u "{MYSQL_USER}" -p"{password}" '
                f'-h "{MYSQL_HOST}" -P "{MYSQL_PORT}" "{database}" > "{sql_file}"'
            )
            subprocess.run(comando, shell=True, check=False)

            gz_file = Path(f'{sql_file}.gz')
            with open(sql_file, 'rb') as f_in:
                with gzip.open(gz_file, 'wb') as f_out:
                    f_out.writelines(f_in)
            sql_file.unlink(missing_ok=True)
            detalles.append(str(gz_file.name))

        return '✅ Backup automático creado correctamente', detalles

    except Exception as e:
        return f'❌ Error automático: {str(e)}', []
