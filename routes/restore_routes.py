from flask import Blueprint, request, redirect
from utils.restore_utils import restaurar_backup
from utils.log_utils import guardar_log

restore_bp = Blueprint('restore', __name__)


@restore_bp.route('/restore', methods=['POST'])
def restore():

    archivo = request.files['archivo']

    resultado = restaurar_backup(
        archivo,
        'toor'
    )

    guardar_log(f'RESTORE | {resultado}')

    return redirect(f'/?mensaje={resultado}')