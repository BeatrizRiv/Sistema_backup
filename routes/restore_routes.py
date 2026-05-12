from flask import Blueprint, request, redirect
from db import MYSQL_PASSWORD
from utils.auth_utils import login_required
from utils.restore_utils import restaurar_backup
from utils.log_utils import guardar_log

restore_bp = Blueprint('restore', __name__)


@restore_bp.route('/restore', methods=['POST'])
@login_required
def restore():

    archivo = request.files['archivo']

    resultado = restaurar_backup(
        archivo,
        MYSQL_PASSWORD
    )

    guardar_log(f'RESTORE | {resultado}')

    return redirect(f'/?mensaje={resultado}')