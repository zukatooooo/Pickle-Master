from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FileField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired


class AddProductForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    price = IntegerField("Price", validators=[DataRequired()])
    image = FileField("image", validators=[DataRequired()])
    submit = SubmitField('Add Product')
