from blueprints.auth.models import User
from blueprints.auth.forms import AuthLoginForm, AuthRegisterForm
from blueprints.auth.utils import login_required
from flask import Blueprint, render_template, redirect, request, session, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash


auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
User.create_table()


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = AuthRegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = form.password.data
        hashed_password = generate_password_hash(password)

        existing_users = User.filter(email=email)
        if existing_users:
            flash('User with this email already registered', 'danger')
            return redirect(url_for('auth.register'))

        is_admin = False
        if email == 'admin@localhost.com':
            is_admin = True

        User.create(
            name=name,
            email=email,
            password=hashed_password,
            is_admin=is_admin
        )

        flash('User successfully registered!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = AuthLoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        try:
            user = User.get(email=email)
        except User.DoesNotExist:
            flash('User with this email does not exist', 'danger')
            return redirect(url_for('auth.login'))

        if not check_password_hash(user.password, password):
            flash('Password is not valid', 'danger')
            return redirect(url_for('auth.login'))

        session['user_id'] = user.id
        session['is_admin'] = user.is_admin
        session['is_authenticated'] = True
        return redirect('/')

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect('/')
