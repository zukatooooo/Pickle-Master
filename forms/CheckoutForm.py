from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class CheckoutForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(), Length(min=2, max=50)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = StringField('Address', validators=[DataRequired(), Length(min=2, max=100)])
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=50)])
    zipCode = StringField('Zip Code', validators=[DataRequired()])
    cardName = StringField('Name on Card', validators=[DataRequired(), Length(min=2, max=50)])
    cardNumber = StringField('Credit Card Number', validators=[DataRequired(), Length(min=16, max=16)])
    expiration = StringField('Expiration', validators=[DataRequired(), Length(min=5, max=5)])
    cvv = StringField('CVV', validators=[DataRequired(), Length(min=3, max=4)])
    submit = SubmitField('Place Order')
