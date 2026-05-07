from flask import Blueprint, render_template, request, redirect
from db import conectar, MYSQL_PASSWORD
from utils.backup_utils import crear_backup
from utils.log_utils import guardar_log, obtener_logs

backup_bp = Blueprint('backup', __name__)


@backup_bp.route('/')
def index():

    conexion = conectar()
    cursor = conexion.cursor()
    cursor.execute("SHOW DATABASES")

    bases = [
        db[0] for db in cursor
        if db[0] not in (
            'information_schema',
            'mysql',
            'performance_schema',
            'sys'
        )
    ]

    conexion.close()

    logs = obtener_logs()
    mensaje = request.args.get('mensaje')

    return render_template(
        'index.html',
        bases=bases,
        logs=logs,
        mensaje=mensaje
    )


@backup_bp.route('/backup', methods=['POST'])
def backup():

    database = request.form['database']
    tipo = request.form['type']

    # ✅ AQUÍ ESTÁ LA CORRECCIÓN
    resultado = crear_backup(database, tipo, MYSQL_PASSWORD)

    guardar_log(f'BACKUP | {database} | OK')

    return redirect(f'/?mensaje={resultado}')