import mysql.connector

MYSQL_PASSWORD = "toor"


def obtener_bases():

    conexion = mysql.connector.connect(
        host='localhost',
        user='root',
        password=MYSQL_PASSWORD
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