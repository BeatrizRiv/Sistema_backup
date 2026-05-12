from functools import wraps
from flask import session, redirect, url_for
from config import ADMIN_USER, ADMIN_PASSWORD


def authenticate(username, password):
    return username == ADMIN_USER and password == ADMIN_PASSWORD


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if session.get('user'):
            return view(*args, **kwargs)
        return redirect(url_for('auth.login'))

    return wrapped
