from flask import Flask, render_template, request
import os
from datetime import datetime
import mysql.connector
import gzip
from cryptography.fernet import Fernet

app = Flask(__name__)

BACKUP_FOLDER = 'backups'
UPLOAD_FOLDER = 'uploads'

os.makedirs(BACKUP_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# CLAVE DE CIFRADO
clave = Fernet.generate_key()
fernet = Fernet(clave)


@app.route('/')
def index():

    conexion = mysql.connector.connect(
        host="localhost",
        user="root",
        password="toor"
    )

    cursor = conexion.cursor()

    cursor.execute("SHOW DATABASES")

    bases = []

    for db in cursor:

        nombre = db[0]

        if nombre not in [
            'information_schema',
            'mysql',
            'performance_schema',
            'sys'
        ]:

            bases.append(nombre)

    conexion.close()

    return render_template(
        'index.html',
        bases=bases
    )


@app.route('/backup', methods=['POST'])
def backup():

    database = request.form['database']
    backup_type = request.form['type']

    fecha = datetime.now().strftime('%Y%m%d_%H%M%S')

    sql_file = f'{BACKUP_FOLDER}/{database}_{fecha}.sql'

    # CREAR SQL
    os.system(
        f'mysqldump -u root -ptoor {database} > "{sql_file}"'
    )

    resultado = ''

    # SOLO SQL
    if backup_type == 'sql':

        resultado = f'Backup SQL creado: {sql_file}'

    # GZIP
    elif backup_type == 'gz':

        gz_file = f'{sql_file}.gz'

        with open(sql_file, 'rb') as f_in:
            with gzip.open(gz_file, 'wb') as f_out:
                f_out.writelines(f_in)

        os.remove(sql_file)

        resultado = f'Backup comprimido creado: {gz_file}'

    # CIFRADO
    elif backup_type == 'enc':

        # COMPRESIÓN
        gz_file = f'{sql_file}.gz'

        with open(sql_file, 'rb') as f_in:
            with gzip.open(gz_file, 'wb') as f_out:
                f_out.writelines(f_in)

        # CIFRADO
        with open(gz_file, 'rb') as archivo:
            datos = archivo.read()

        datos_cifrados = fernet.encrypt(datos)

        enc_file = f'{BACKUP_FOLDER}/{database}_{fecha}.enc'

        with open(enc_file, 'wb') as archivo:
            archivo.write(datos_cifrados)

        os.remove(sql_file)
        os.remove(gz_file)

        resultado = f'Backup cifrado creado: {enc_file}'

    return f'''
    <h2>{resultado}</h2>
    <br>
    <a href="/">Volver</a>
    '''


@app.route('/restore', methods=['POST'])
def restore():

    database = request.form['restore_database']

    archivo = request.files['file']

    if archivo.filename == '':
        return 'No seleccionaste archivo'

    ruta = os.path.join(
        UPLOAD_FOLDER,
        archivo.filename
    )

    archivo.save(ruta)

    nombre = archivo.filename.lower()

    # SQL
    if nombre.endswith('.sql'):

        os.system(
            f'mysql -u root -ptoor {database} < "{ruta}"'
        )

        mensaje = 'Base restaurada desde SQL'

    # GZ
    elif nombre.endswith('.gz'):

        sql_file = ruta.replace('.gz', '')

        with gzip.open(ruta, 'rb') as f_in:
            with open(sql_file, 'wb') as f_out:
                f_out.write(f_in.read())

        os.system(
            f'mysql -u root -ptoor {database} < "{sql_file}"'
        )

        mensaje = 'Base restaurada desde GZIP'

    # ENC
    elif nombre.endswith('.enc'):

        with open(ruta, 'rb') as archivo:
            datos_cifrados = archivo.read()

        datos = fernet.decrypt(datos_cifrados)

        gz_file = ruta.replace('.enc', '.sql.gz')

        with open(gz_file, 'wb') as archivo:
            archivo.write(datos)

        sql_file = gz_file.replace('.gz', '')

        with gzip.open(gz_file, 'rb') as f_in:
            with open(sql_file, 'wb') as f_out:
                f_out.write(f_in.read())

        os.system(
            f'mysql -u root -ptoor {database} < "{sql_file}"'
        )

        mensaje = 'Base restaurada desde archivo cifrado'

    else:

        mensaje = 'Formato no soportado'

    return f'''
    <h2>{mensaje}</h2>
    <br>
    <a href="/">Volver</a>
    '''


if __name__ == '__main__':
    app.run(debug=True)