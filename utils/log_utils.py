import os
from datetime import datetime

LOG_FOLDER = 'logs'

LOG_FILE = 'logs/logs.txt'

os.makedirs(LOG_FOLDER, exist_ok=True)

if not os.path.exists(LOG_FILE):

    with open(LOG_FILE, 'w') as f:
        pass


def guardar_log(mensaje):

    fecha = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    with open(LOG_FILE, 'a', encoding='utf-8') as archivo:

        archivo.write(f'{fecha} | {mensaje}\n')


def obtener_logs():

    with open(LOG_FILE, 'r', encoding='utf-8') as archivo:

        lineas = archivo.readlines()

    lineas.reverse()

    return lineas[:10]