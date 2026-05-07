from flask import Blueprint, request, redirect
from utils.restore_utils import restaurar_backup
from utils.log_utils import guardar_log

restore_bp = Blueprint('restore', __name__)


@restore_bp.route('/restore', methods=['POST'])
def restore():

    database = request.form['restore_database']
    archivo = request.files['file']

    resultado = restaurar_backup(database, archivo)

    guardar_log(f'RESTORE | {database} | OK')

    return redirect(f'/?mensaje={resultado}')