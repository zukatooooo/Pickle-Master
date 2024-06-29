from ext import app, db
from models.Product import Product
from models.User import User
from models.Cart import Cart
from models.Favorite import Favorite

with app.app_context():

    db.drop_all()
    db.create_all()
