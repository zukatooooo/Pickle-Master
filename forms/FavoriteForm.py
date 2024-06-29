from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField


class FavoriteForm(FlaskForm):
    productId = StringField()
    addToCart = SubmitField('Add to cart')
    delete = SubmitField('X')
