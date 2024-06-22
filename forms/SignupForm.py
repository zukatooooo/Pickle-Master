from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, length, equal_to


class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password1 = PasswordField("Password", validators=[DataRequired(), length(min=8, message="Password to short")])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), equal_to("password1",
                                                                                      message="Passwords don't match")])
    submit = SubmitField('Sign Up')
