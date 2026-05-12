from flask import Blueprint, render_template, request, redirect, url_for, session
from utils.auth_utils import authenticate

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if authenticate(username, password):
            session['user'] = username
            return redirect(url_for('backup_bp.index'))

        error = 'Usuario o contraseña inválidos'

    return render_template('login.html', error=error)


@auth_bp.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('auth.login'))
