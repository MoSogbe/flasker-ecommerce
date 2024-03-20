from market import app
from flask import render_template, redirect, url_for, flash, get_flashed_messages, request
from sqlalchemy.exc import SQLAlchemyError
from market.models import Item,User
from market import db
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from flask_login import login_user, logout_user, login_required, current_user
@app.route("/")
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market', methods=['GET','POST'])
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        #Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category='danger')
        #Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations! You sold {s_item_object.name} back to market!", category='success')
            else:
                flash(f"Something went wrong with selling {s_item_object.name}", category='danger')


        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)
        return render_template('market.html', items=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form)
        
    
@app.route('/register', methods = ['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,email_address= form.email_address.data,password = form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Accounted created successfuly. You are now logded in as : {user_to_create.username}',category='success')
        return redirect(url_for('market_page'))
    if form.errors != {}: #if there are no errors in the validation
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user {err_msg}', category='danger')
    return render_template('register.html', form=form)
    
    
@app.route('/login', methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
            attempted_password = form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are login in as : {attempted_user.username}',category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are match! Please try again', category='danger')
    return render_template('login.html', form=form)
    
@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been logout!', category='info')
    return redirect(url_for("home_page"))
    


@app.route("/run-db")
def run_db():
    with app.app_context():
    # Perform database operations
        #u1= User(username='mohammed',password_hash='123456',email_address='mohammed@noodala.com',budget=100)
        # i1 = Item(name='Laptop', description='description2',barcode='12456789',price=800)
        # db.session.add(i1)
        # db.session.commit()
        item1 = Item.query.filter_by(name='Iphone 10').first()
        user1 =  User.query.filter_by(username='jsc').first()
        item1.owner =user1.id
        db.session.add(item1)
        db.session.commit()
        
        return item1