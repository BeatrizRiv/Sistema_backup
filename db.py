import mysql.connector
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_PORT


def obtener_bases():

    try:

        conexion = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            port=MYSQL_PORT,
        )

        cursor = conexion.cursor()

        cursor.execute('SHOW DATABASES')

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

        return bases

    except mysql.connector.Error as e:

        raise RuntimeError(f'Error de conexión MySQL: {e}')
