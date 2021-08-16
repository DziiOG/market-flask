from src import app
from flask import render_template, redirect, url_for, flash, request
from src.models.item import Item
from src.helpers.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from src.models.user import User
from src import db
from flask_login import login_user, logout_user, login_required, current_user
#decorator
#functions that execute before the routes
#routes

@app.route('/')
@app.route('/home')
def home_page():
    """home route fuction"""
    return render_template('home.html', title="Home")


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    """market route fuction"""
    purchase_form = PurchaseItemForm()
    sell_form = SellItemForm()

    if request.method == "POST":
            purchased_item = request.form.get('purchased_item')
            if purchased_item:
                p_item_obj = Item.query.filter_by(name=purchased_item).first()
                if p_item_obj:
                    if current_user.can_purchase(p_item_obj):
                        p_item_obj.buy(current_user)
                        flash(f"Congratulations! You purchased {p_item_obj.name} for {p_item_obj.price}", category="success")
                    else: 
                        flash(f"Unfortunately, you dont have enough money to purchase {p_item_obj.name}", category="danger")

                return redirect(url_for('market_page'))
        
      
            selling_item = request.form.get('sold_item')
            if selling_item:
                s_item_obj = Item.query.filter_by(name=selling_item).first()
                if s_item_obj:
                    s_item_obj.sell(current_user)
                    flash(f"Congratulations! You sold {s_item_obj.name} for {s_item_obj.price}", category="success")
                
                return redirect(url_for('market_page'))

    if request.method == 'GET':
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, sell_form=sell_form, owned_items=owned_items, title="Market")

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user_to_create)
        db.session.commit()

         #login the user
        login_user(user_to_create)
        #flash a message about being successful
        flash(f'Account created successfully you are now logged as, {user_to_create.username}', category='success')

        return redirect(url_for('market_page'))
    
    if form.errors != {}: #if there are no errors from validations
        for err_msg in form.errors.values():
            flash(f'There was an error in creating a user: {err_msg[0]}', category='danger')
    return render_template('register.html', form=form, title="Register")


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        #check if the user exists
        attempted_user = User.query.filter_by(username=form.username.data).first()
        #if the user exits and the password matches hashed password in db
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            #login the user
            login_user(attempted_user)
            #flash a message about being successful
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            #redirect the user to the market page route
            return redirect(url_for('market_page'))
        else:
            #flash error if user does not exist or is incorrect
            flash('User and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form, title="Login")


@app.route('/logout', methods=['GET', 'POST'])
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('home_page'))