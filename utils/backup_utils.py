import os
import gzip
from datetime import datetime
from utils.crypto_utils import fernet

BACKUP_FOLDER = 'backups'

os.makedirs(BACKUP_FOLDER, exist_ok=True)


def crear_backup(database, tipo, password):

    fecha = datetime.now().strftime('%Y%m%d_%H%M%S')

    sql_file = f'{BACKUP_FOLDER}/{database}_{fecha}.sql'

    os.system(
        f'mysqldump -u root -p{password} {database} > "{sql_file}"'
    )

    if tipo == 'sql':

        return 'Backup SQL creado correctamente'

    elif tipo == 'gz':

        gz_file = f'{sql_file}.gz'

        with open(sql_file, 'rb') as f_in:
            with gzip.open(gz_file, 'wb') as f_out:
                f_out.writelines(f_in)

        os.remove(sql_file)

        return 'Backup comprimido creado correctamente'

    elif tipo == 'enc':

        gz_file = f'{sql_file}.gz'

        with open(sql_file, 'rb') as f_in:
            with gzip.open(gz_file, 'wb') as f_out:
                f_out.writelines(f_in)

        with open(gz_file, 'rb') as archivo:
            datos = archivo.read()

        datos_cifrados = fernet.encrypt(datos)

        enc_file = f'{BACKUP_FOLDER}/{database}_{fecha}.enc'

        with open(enc_file, 'wb') as archivo:
            archivo.write(datos_cifrados)

        os.remove(sql_file)

        os.remove(gz_file)

        return 'Backup cifrado creado correctamente'