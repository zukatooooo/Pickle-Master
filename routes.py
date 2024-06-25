from os import path

from flask import render_template, redirect, url_for, flash
from flask_login import login_user, login_required, current_user, logout_user

from ext import app, db
from forms.AddProductForm import AddProductForm
from forms.LoginForm import LoginForm
from forms.ProductForm import ProductForm
from forms.SearchForm import SearchForm
from forms.SignupForm import SignupForm
from models.Cart import Cart
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
                add_to_cart = Cart(user_id=current_user.id, product_id=product_form.productId.data)
                db.session.add(add_to_cart)
                db.session.commit()
                return redirect(url_for('home'))
            elif product_form.favorite.data:
                print("favorite")
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
    if current_user.is_authenticated:
        products = db.session.query(Product).join(Cart).filter(Cart.user_id == current_user.id).all()
        total_price = sum(product.price for product in products)
        return render_template('cart.html', search_form=search_form, products=products, total_price=total_price)
    else:
        return redirect(url_for("login"))
