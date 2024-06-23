from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "35XC465V&b^*yNBV65CR45X3C4V57b687n*B^&V%C$#%3C$^%V&B^*Nb865v74c6x3c465v7b68n"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///pickle_master.db"

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = "login"
