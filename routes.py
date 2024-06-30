from os import path

from flask import render_template, redirect, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user

from ext import app, db
from forms.AddProductForm import AddProductForm
from forms.CartForm import CartForm
from forms.CheckoutForm import CheckoutForm
from forms.ContactForm import ContactForm
from forms.DeleteForm import DeleteForm
from forms.FavoriteForm import FavoriteForm
from forms.LoginForm import LoginForm
from forms.ProductForm import ProductForm
from forms.SearchForm import SearchForm
from forms.SignupForm import SignupForm
from models.Cart import Cart
from models.Favorite import Favorite
from models.Product import Product
from models.User import User


@app.route("/", methods=['GET', 'POST'])
def home():
    search_form = SearchForm()
    product_form = ProductForm()

    if search_form.validate_on_submit():
        search_query = search_form.searchBar.data
        products = Product.query.filter(Product.name.ilike(f"%{search_query}%")).all()
    else:
        products = Product.query.all()

    if current_user.is_authenticated:
        if product_form.validate_on_submit():
            if product_form.addToCart.data:

                existing_cart = Cart.query.filter_by(user_id=current_user.id, product_id=product_form.productId.data).first()
                if existing_cart:
                    return redirect(url_for('home'))

                add_to_cart = Cart(user_id=current_user.id, product_id=product_form.productId.data)
                db.session.add(add_to_cart)
                db.session.commit()
                return redirect(url_for('home'))

            elif product_form.favorite.data:

                existing_favorite = Favorite.query.filter_by(user_id=current_user.id, product_id=product_form.productId.data).first()
                if existing_favorite:
                    return redirect(url_for('home'))

                new_favorite = Favorite(user_id=current_user.id, product_id=product_form.productId.data)
                db.session.add(new_favorite)
                db.session.commit()

                return redirect(url_for('home'))

    return render_template("home.html", products=products, search_form=search_form, product_form=product_form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = SignupForm()
    search_form = SearchForm()
    if signup_form.validate_on_submit():

        if User.query.filter_by(username=signup_form.username.data).first():
            flash('Username is already in use', 'danger')
            return redirect(url_for('signup'))

        if User.query.filter_by(email=signup_form.email.data).first():
            flash('Email is already in use', 'danger')
            return redirect(url_for('signup'))

        new_user = User(username=signup_form.username.data, email=signup_form.email.data, password=signup_form.password1.data, role="User")

        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', signup_form=signup_form, search_form=search_form)


@app.route("/login", methods=["GET", "POST"])
def login():
    search_form = SearchForm()

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter(User.username == login_form.username.data).first()
        if user and user.check_password(login_form.password.data):
            login_user(user)
            return redirect("/")
    return render_template("login.html", login_form=login_form, search_form=search_form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")


@app.route('/addProduct', methods=['GET', 'POST'])
@login_required
def add_product():
    search_form = SearchForm()
    add_product_form = AddProductForm()
    if add_product_form.validate_on_submit():
        new_product = Product(name=add_product_form.name.data, price=add_product_form.price.data)

        image = add_product_form.image.data
        directory = path.join(app.root_path, "static", "images", image.filename)
        image.save(directory)

        new_product.image = image.filename

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('home'))
    return render_template('add_product.html', add_product_form=add_product_form, search_form=search_form)


@app.route('/cart', methods=['GET', 'POST'])
def cart():
    search_form = SearchForm()
    cart_form = CartForm()
    if current_user.is_authenticated:
        products = db.session.query(Product).join(Cart).filter(Cart.user_id == current_user.id).all()
        total_price = sum(product.price for product in products)
        if cart_form.validate_on_submit():
            if cart_form.removeFromCart:
                Cart.query.filter_by(user_id=current_user.id, product_id=cart_form.productId.data).delete()
                db.session.commit()
                return redirect(url_for("cart"))

        return render_template('cart.html', search_form=search_form, cart_form=cart_form, products=products, total_price=total_price)
    else:
        return redirect(url_for("login"))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    search_form = SearchForm()
    checkout_form = CheckoutForm()
    if checkout_form.validate_on_submit():
        Cart.query.filter_by(user_id=current_user.id).delete()
        db.session.commit()

        return redirect(url_for('order_confirmation'))

    return render_template('checkout.html', search_form=search_form, checkout_form=checkout_form)


@app.route('/orderConfirmation')
def order_confirmation():
    search_form = SearchForm()
    return render_template('order_confirmation.html', search_form=search_form)


@app.route('/deleteProduct', methods=['GET', 'POST'])
@login_required
def delete():

    products = Product.query.all()

    search_form = SearchForm()
    delete_form = DeleteForm()

    if delete_form.validate_on_submit():
        if delete_form.delete.data:

            Product.query.filter_by(id=delete_form.productId.data).delete()
            db.session.commit()

            return redirect(url_for('delete'))
    return render_template('delete_product.html', search_form=search_form, favorite_form=delete_form, products=products)


@app.route('/favorite', methods=['GET', 'POST'])
@login_required
def favorite():
    products = db.session.query(Product).join(Favorite).filter(Favorite.user_id == current_user.id).all()

    search_form = SearchForm()
    favorite_form = FavoriteForm()

    if favorite_form.validate_on_submit():
        if favorite_form.addToCart.data:

            existing_cart = Cart.query.filter_by(user_id=current_user.id, product_id=favorite_form.productId.data).first()
            if existing_cart:
                return redirect(url_for('favorite'))

            add_to_cart = Cart(user_id=current_user.id, product_id=favorite_form.productId.data)
            db.session.add(add_to_cart)
            db.session.commit()
            return redirect(url_for('favorite'))

        elif favorite_form.delete.data:

            Favorite.query.filter_by(user_id=current_user.id, product_id=favorite_form.productId.data).delete()
            db.session.commit()

            return redirect(url_for('favorite'))

    return render_template('favorite.html', search_form=search_form, products=products, favorite_form=favorite_form)


@app.route('/about')
def about():
    search_form = SearchForm()
    return render_template('about.html', search_form=search_form)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    search_form = SearchForm()
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        return redirect("/")
    return render_template("contact.html", contact_form=contact_form, search_form=search_form)
