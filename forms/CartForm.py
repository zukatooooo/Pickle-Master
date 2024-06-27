from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import SubmitField


class CartForm(FlaskForm):
    productId = StringField()
    removeFromCart = SubmitField('X')
