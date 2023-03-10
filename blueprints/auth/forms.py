from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class AuthLoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password = StringField('password', validators=[DataRequired(), Length(min=3, max=20)])


class AuthRegisterForm(AuthLoginForm):
    name = StringField('name', validators=[DataRequired(), Length(min=3, max=50)])
    confirm_password = StringField('confirm_password', validators=[DataRequired(), Length(min=3, max=20), EqualTo('password', 'Passwords do not match')])
