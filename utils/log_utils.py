from datetime import datetime

LOG_FILE = r'C:\Users\Beatriz\OneDrive\Escritorio\SistemaBackup\logs\logs.txt'


def guardar_log(mensaje):

    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(LOG_FILE, 'a', encoding='utf-8') as archivo:

        archivo.write(f'{fecha} | {mensaje}\n')


def obtener_logs():

    try:

        with open(LOG_FILE, 'r', encoding='utf-8') as archivo:

            lineas = archivo.readlines()

        lineas.reverse()

        return lineas[:10]

    except:

        return []