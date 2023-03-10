from flask_wtf import FlaskForm
from wtforms.fields import IntegerField
from wtforms.validators import DataRequired, NumberRange


class CartItemEditForm(FlaskForm):
    amount = IntegerField('amount', validators=[DataRequired(), NumberRange(min=1)])
