import os

from flask import Flask, render_template, request, flash, redirect, session, g 
# from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Brewery, Review, states_list, type_list
from forms import UserAddForm, LoginForm
from config import Config, DevelopmentConfig, ProductionConfig, TestingConfig

CURR_USER_KEY = 'curr_user'

app = Flask(__name__)
app.app_context().push()

if app.config['ENV'] == 'development':
    app.config.from_object(DevelopmentConfig)
else: 
    app.config.from_object(TestingConfig)

connect_db(app)


##############################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """ if logged in add user to Flask global """

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """ Log in user """

    session[CURR_USER_KEY] = user.id

def do_logout():
    """ Logout user"""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """ Handle signup """

    form = UserAddForm()
    form.state.choices = states_list()
    form.fav_type.choices = type_list()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,    
                city=form.city.data,
                state=form.state.data,
                postal_code=form.postal_code.data,
                fav_type=form.fav_type.data
            )
            db.session.commit()
        except:
            return render_template('signup.html', form=form)

        do_login(user)
        return redirect('/')

    else:
        return render_template('signup.html', form=form)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Handle login """

    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            return redirect('/')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """ Handle logout """
    
    do_logout()

    return redirect('/login')

@app.route('/')
def index():
    """ Homepage for Hoppy Hour """


    return render_template('base.html')

