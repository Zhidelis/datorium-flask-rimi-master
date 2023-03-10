from functools import wraps
from flask import session, request, redirect, url_for


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_authenticated', None):
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function