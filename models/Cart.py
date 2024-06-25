from ext import db


class Cart(db.Model):

    __tablename__ = "cart"

    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)

    user = db.relationship('User', back_populates='cart')
    product = db.relationship('Product', back_populates='cart')
