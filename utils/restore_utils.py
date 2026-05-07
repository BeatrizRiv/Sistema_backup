import os
import gzip
from utils.crypto_utils import fernet

UPLOAD_FOLDER = 'uploads'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def restaurar_backup(database, archivo, password):

    ruta = os.path.join(
        UPLOAD_FOLDER,
        archivo.filename
    )

    archivo.save(ruta)

    nombre = archivo.filename.lower()

    if nombre.endswith('.sql'):

        os.system(
            f'mysql -u root -p{password} {database} < "{ruta}"'
        )

        return 'Base restaurada desde SQL'

    elif nombre.endswith('.gz'):

        sql_file = ruta.replace('.gz', '')

        with gzip.open(ruta, 'rb') as f_in:
            with open(sql_file, 'wb') as f_out:
                f_out.write(f_in.read())

        os.system(
            f'mysql -u root -p{password} {database} < "{sql_file}"'
        )

        return 'Base restaurada desde GZIP'

    elif nombre.endswith('.enc'):

        with open(ruta, 'rb') as archivo_enc:
            datos_cifrados = archivo_enc.read()

        datos = fernet.decrypt(datos_cifrados)

        gz_file = ruta.replace('.enc', '.sql.gz')

        with open(gz_file, 'wb') as archivo_gz:
            archivo_gz.write(datos)

        sql_file = gz_file.replace('.gz', '')

        with gzip.open(gz_file, 'rb') as f_in:
            with open(sql_file, 'wb') as f_out:
                f_out.write(f_in.read())

        os.system(
            f'mysql -u root -p{password} {database} < "{sql_file}"'
        )

        return 'Base restaurada desde archivo cifrado'

    return 'Formato no soportado'