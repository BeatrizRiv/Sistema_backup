from flask import Blueprint, render_template, request, redirect, send_file
from db import obtener_bases, MYSQL_PASSWORD
from utils.backup_utils import crear_backup
from utils.log_utils import guardar_log, obtener_logs

backup_bp = Blueprint('backup_bp', __name__)

ultimo_backup = None


@backup_bp.route('/')
def index():

    bases = obtener_bases()

    logs = obtener_logs()

    mensaje = request.args.get('mensaje')

    return render_template(
        'index.html',
        databases=bases,
        logs=logs,
        mensaje=mensaje
    )


@backup_bp.route('/backup', methods=['POST'])
def backup():

    global ultimo_backup

    database = request.form['database']

    tipo = request.form['tipo']

    resultado, ruta = crear_backup(
        database,
        tipo,
        MYSQL_PASSWORD
    )

    ultimo_backup = ruta

    guardar_log(f'{resultado} | {database}')

    return redirect(f'/?mensaje={resultado}')


@backup_bp.route('/download')
def download():

    global ultimo_backup

    return send_file(
        ultimo_backup,
        as_attachment=True
    )