from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    FloatField,
    IntegerField,
    BooleanField
)
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import DataRequired, Length, Optional, NumberRange
from app import app


class AdminProductForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=3, max=150)])
    price = FloatField('price', validators=[DataRequired(), NumberRange(min=0)])
    description = StringField('description', validators=[DataRequired(), Length(min=10, max=1000)])
    image = FileField('image', validators=[
        FileRequired(),
        FileAllowed(app.config['VALID_IMAGE_FORMATS'])
    ])
    stock = IntegerField('stock', validators=[DataRequired(), NumberRange(min=0)])
    hidden = BooleanField('hidden', default=False, validators=[Optional()])


class AdminProductEditForm(AdminProductForm):
    image = FileField('image', validators=[
        Optional(),
        FileAllowed(app.config['VALID_IMAGE_FORMATS'])
    ])
