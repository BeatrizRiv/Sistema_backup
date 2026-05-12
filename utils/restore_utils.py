import os
import re
import gzip
import subprocess
from utils.crypto_utils import fernet

UPLOAD_FOLDER = 'uploads'

MYSQL_PATH = r'"C:\Program Files\MySQL\MySQL Server 9.2\bin\mysql.exe"'


def crear_base(database, password):

    comando = (
        f'{MYSQL_PATH} -u root -p{password} '
        f'-e "CREATE DATABASE IF NOT EXISTS `{database}`"'
    )

    subprocess.run(
        comando,
        shell=True,
        check=False
    )


def extraer_nombre_bd(nombre_archivo):

    if nombre_archivo.endswith('.enc'):
        nombre_base = nombre_archivo[:-4]
    elif nombre_archivo.endswith('.gz'):
        nombre_base = nombre_archivo[:-3]
    elif nombre_archivo.endswith('.sql'):
        nombre_base = nombre_archivo[:-4]
    else:
        nombre_base = nombre_archivo

    nombre_base = re.sub(r'_(\d{8}_\d{6})$', '', nombre_base)

    return nombre_base


def restaurar_backup(archivo, password):

    nombre = archivo.filename.lower()

    extensiones_validas = (
        '.sql',
        '.gz',
        '.enc'
    )

    if not nombre.endswith(extensiones_validas):

        return '❌ Formato no permitido. Solo se aceptan .sql, .gz y .enc'

    ruta = os.path.join(
        UPLOAD_FOLDER,
        archivo.filename
    )

    archivo.save(ruta)

    database = extraer_nombre_bd(nombre)

    crear_base(database, password)

    if nombre.endswith('.sql'):

        comando = (
            f'{MYSQL_PATH} -u root -p{password} '
            f'{database} < "{ruta}"'
        )

        subprocess.run(
            comando,
            shell=True
        )

        return f'✅ Base restaurada desde SQL: {database}'

    elif nombre.endswith('.gz'):

        sql_file = ruta[:-3]

        with gzip.open(ruta, 'rb') as f_in:
            with open(sql_file, 'wb') as f_out:
                f_out.write(f_in.read())

        comando = (
            f'{MYSQL_PATH} -u root -p{password} '
            f'{database} < "{sql_file}"'
        )

        subprocess.run(
            comando,
            shell=True
        )

        return f'✅ Base restaurada desde archivo cifrado: {database}'

    elif nombre.endswith('.enc'):

        with open(ruta, 'rb') as archivo_enc:
            datos_cifrados = archivo_enc.read()

        datos = fernet.decrypt(datos_cifrados)

        gz_file = ruta[:-4] + '.sql.gz'

        with open(gz_file, 'wb') as archivo_gz:
            archivo_gz.write(datos)

        sql_file = gz_file[:-3]

        with gzip.open(gz_file, 'rb') as f_in:
            with open(sql_file, 'wb') as f_out:
                f_out.write(f_in.read())

        comando = (
            f'{MYSQL_PATH} -u root -p{password} '
            f'{database} < "{sql_file}"'
        )

        subprocess.run(
            comando,
            shell=True
        )

        return '✅ Base restaurada desde archivo cifrado'