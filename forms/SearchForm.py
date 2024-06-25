from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import SubmitField


class SearchForm(FlaskForm):
    search_bar = StringField('Search bar')
    search_button = SubmitField('Search')
