import os
import gzip
import mysql.connector
from datetime import datetime
from utils.crypto_utils import fernet

BACKUP_FOLDER = r'C:\Users\Beatriz\OneDrive\Escritorio\SistemaBackup\backups'


def crear_backup(database, tipo, password):

    try:

        conexion = mysql.connector.connect(
            host='localhost',
            user='root',
            password=password
        )

        cursor = conexion.cursor()

        cursor.execute('SHOW DATABASES')

        bases = [db[0] for db in cursor]

        conexion.close()

        if database not in bases:

            return '❌ La base de datos no existe', None

        fecha = datetime.now().strftime('%Y%m%d_%H%M%S')

        sql_file = os.path.join(
            BACKUP_FOLDER,
            f'{database}_{fecha}.sql'
        )

        comando = (
            f'mysqldump -u root -ptoor '
            f'{database} > "{sql_file}"'
        )

        os.system(comando)

        if tipo == 'sql':

            return '✅ Backup SQL creado correctamente', sql_file

        elif tipo == 'gz':

            gz_file = f'{sql_file}.gz'

            with open(sql_file, 'rb') as f_in:
                with gzip.open(gz_file, 'wb') as f_out:
                    f_out.writelines(f_in)

            os.remove(sql_file)

            return '✅ Backup comprimido creado correctamente', gz_file

        elif tipo == 'enc':

            gz_file = f'{sql_file}.gz'

            with open(sql_file, 'rb') as f_in:
                with gzip.open(gz_file, 'wb') as f_out:
                    f_out.writelines(f_in)

            with open(gz_file, 'rb') as archivo:
                datos = archivo.read()

            datos_cifrados = fernet.encrypt(datos)

            enc_file = os.path.join(
                BACKUP_FOLDER,
                f'{database}_{fecha}.enc'
            )

            with open(enc_file, 'wb') as archivo:
                archivo.write(datos_cifrados)

            os.remove(sql_file)

            os.remove(gz_file)

            return '✅ Backup cifrado creado correctamente', enc_file

    except Exception as e:

        return f'❌ Error: {str(e)}', None