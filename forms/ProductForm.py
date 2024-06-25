from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField


class ProductForm(FlaskForm):
    productId = StringField()
    addToCart = SubmitField('Add to cart')
    favorite = SubmitField('❤')
