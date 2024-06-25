from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.fields.simple import SubmitField


class SearchForm(FlaskForm):
    searchBar = StringField('Search bar')
    searchButton = SubmitField('Search')
