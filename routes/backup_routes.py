from flask import Blueprint, render_template, request, redirect, send_file, session, url_for
from db import obtener_bases, MYSQL_PASSWORD
from utils.backup_utils import crear_backup, crear_backup_automatico
from utils.auth_utils import login_required
from utils.dashboard_utils import obtener_estadisticas
from utils.log_utils import guardar_log, obtener_logs

backup_bp = Blueprint('backup_bp', __name__)

ultimo_backup = None


@backup_bp.route('/')
@login_required
def index():

    try:
        bases = obtener_bases()
        stats = obtener_estadisticas()
        mensaje = request.args.get('mensaje')

    except RuntimeError as e:
        bases = []
        stats = {
            'total_backups': 0,
            'total_size': '0 B',
            'ultimo_backup': 'N/A',
            'ultimo_backup_fecha': 'N/A',
            'ultima_restauracion': 'N/A',
            'estado_sistema': str(e),
        }
        mensaje = f'❌ {e}'

    logs = obtener_logs()

    return render_template(
        'index.html',
        databases=bases,
        logs=logs,
        mensaje=mensaje,
        stats=stats,
        user=session.get('user')
    )


@backup_bp.route('/backup', methods=['POST'])
@login_required
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


@backup_bp.route('/auto-backup', methods=['POST'])
@login_required
def auto_backup():

    resultado, detalles = crear_backup_automatico(MYSQL_PASSWORD)
    guardar_log(f'{resultado} | {"; ".join(detalles)}')

    return redirect(f'/?mensaje={resultado}')


@backup_bp.route('/download')
@login_required
def download():

    global ultimo_backup

    return send_file(
        ultimo_backup,
        as_attachment=True
    )