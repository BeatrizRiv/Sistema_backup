import gzip
import re
import subprocess
import time
from pathlib import Path
from werkzeug.utils import secure_filename
from utils.crypto_utils import fernet
from config import (
    UPLOAD_FOLDER,
    MYSQL_PATH,
    MYSQL_HOST,
    MYSQL_USER,
    MYSQL_PASSWORD,
    MYSQL_PORT,
)


def crear_base(database, password):
    comando = (
        f'"{MYSQL_PATH}" -u "{MYSQL_USER}" -p"{password}" '
        f'-h "{MYSQL_HOST}" -P "{MYSQL_PORT}" '
        f'-e "CREATE DATABASE IF NOT EXISTS `{database}`"'
    )
    subprocess.run(comando, shell=True, check=False)


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
    nombre = secure_filename(archivo.filename).lower()
    extensiones_validas = ('.sql', '.gz', '.enc')

    if not nombre.endswith(extensiones_validas):
        return '❌ Formato no permitido. Solo se aceptan .sql, .gz y .enc'

    ruta = UPLOAD_FOLDER / nombre
    archivo.save(str(ruta))

    database = extraer_nombre_bd(nombre)
    crear_base(database, password)

    inicio = time.perf_counter()

    if nombre.endswith('.sql'):
        comando = (
            f'"{MYSQL_PATH}" -u "{MYSQL_USER}" -p"{password}" '
            f'-h "{MYSQL_HOST}" -P "{MYSQL_PORT}" "{database}" < "{ruta}"'
        )
        subprocess.run(comando, shell=True, check=False)
        duracion = time.perf_counter() - inicio
        return f'✅ Base restaurada desde SQL: {database} (en {duracion:.2f}s)'

    elif nombre.endswith('.gz'):
        sql_file = ruta.with_suffix('')
        with gzip.open(ruta, 'rb') as f_in:
            with open(sql_file, 'wb') as f_out:
                f_out.write(f_in.read())

        comando = (
            f'"{MYSQL_PATH}" -u "{MYSQL_USER}" -p"{password}" '
            f'-h "{MYSQL_HOST}" -P "{MYSQL_PORT}" "{database}" < "{sql_file}"'
        )
        subprocess.run(comando, shell=True, check=False)
        sql_file.unlink(missing_ok=True)
        duracion = time.perf_counter() - inicio
        return f'✅ Base restaurada desde GZIP: {database} (en {duracion:.2f}s)'

    elif nombre.endswith('.enc'):
        with open(ruta, 'rb') as archivo_enc:
            datos_cifrados = archivo_enc.read()

        datos = fernet.decrypt(datos_cifrados)
        gz_file = ruta.with_suffix('.sql.gz')

        with open(gz_file, 'wb') as archivo_gz:
            archivo_gz.write(datos)

        sql_file = gz_file.with_suffix('')
        with gzip.open(gz_file, 'rb') as f_in:
            with open(sql_file, 'wb') as f_out:
                f_out.write(f_in.read())

        comando = (
            f'"{MYSQL_PATH}" -u "{MYSQL_USER}" -p"{password}" '
            f'-h "{MYSQL_HOST}" -P "{MYSQL_PORT}" "{database}" < "{sql_file}"'
        )
        subprocess.run(comando, shell=True, check=False)
        gz_file.unlink(missing_ok=True)
        sql_file.unlink(missing_ok=True)
        duracion = time.perf_counter() - inicio
        return f'✅ Base restaurada desde archivo cifrado: {database} (en {duracion:.2f}s)'

    return '❌ No se pudo restaurar el archivo'
