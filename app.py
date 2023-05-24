import os, requests, json

from flask import Flask, render_template, request, flash, redirect, session, g 
from sqlalchemy.exc import IntegrityError
from models import db, connect_db, User, Brewery, Review, states_list, type_list, choice_list, rating_list
from forms import UserAddForm, LoginForm, SearchForm, SearchTypeForm, ReviewForm
from config import Config, DevelopmentConfig, ProductionConfig, TestingConfig

CURR_USER_KEY = 'curr_user'
BASE_URL = 'https://api.openbrewerydb.org/v1/breweries'

app = Flask(__name__)
app.app_context().push()

if app.config['ENV'] == 'development':
    app.config.from_object(DevelopmentConfig)
elif app.config['ENV'] == 'production':
    app.config.from_object(ProductionConfig)
else: 
    app.config.from_object(TestingConfig)

google_maps_api_key = os.environ.get('GOOGLE_MAPS_API_KEY')

connect_db(app)


##############################################################################
# User signup/login/logout/edit

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
            flash('signup failed', 'danger')
            return render_template('signup.html', form=form)

        do_login(user)
        flash('signup successful', 'success')
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
            flash('login successful', 'success')
            return redirect('/')
        
        else:
            flash('unsuccessful login', 'danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """ Handle logout """
    
    do_logout()

    return redirect('/login')

@app.route('/edit', methods=['GET', 'POST'])
def get_user():
    """ show user detail """

    if not g.user:
        flash("Access unauthorized. Users can only update their own profile.", "danger")
        return redirect("/")

    user = User.query.get_or_404(g.user.id)
    form = UserAddForm(obj=user)
    form.state.choices = states_list()
    form.fav_type.choices = type_list()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        if user:
            user.username=form.username.data,
            user.email=form.email.data,    
            user.city=form.city.data,
            user.state=form.state.data,
            user.postal_code=form.postal_code.data,
            user.fav_type=form.fav_type.data
            db.session.commit()

            flash('User profile updated successfully', 'success')
            return redirect('/')
    
    return render_template('user-detail.html', form=form)


##############################################################################
# Breweries routes

@app.route('/breweries/<brewery_id>')
def show_breweries(brewery_id):

    try: 
        response = requests.get(f'{BASE_URL}/{brewery_id}')
        if response.status_code == 200:
            brewery = response.json()

    except Exception as e:
        print(e)
        return f'<p>error: {e}</p>'
    
    brewery_reviews = []
    brewery_model = Brewery.query.filter_by(api_id=brewery['id']).first()
    if brewery_model:
        brewery_reviews = Review.query.filter_by(brewery_id=brewery_model.id).order_by(Review.timestamp.desc()).all()

    return render_template('brewery-details.html', brewery=brewery, brewery_reviews=brewery_reviews, google_maps_api_key=google_maps_api_key)


@app.route('/')
def index():
    """ Homepage for Hoppy Hour """

    form = SearchTypeForm()
    form.search_type.choices = choice_list()
    form2 = SearchForm()

    recent_reviews = Review.query.order_by(Review.timestamp.desc()).limit(5)

    return render_template('home.html', form=form, form2=form2, recent_reviews=recent_reviews)


##############################################################################
#Review routes

@app.route('/review/<brewery_id>', methods=["GET", "POST"])
def leave_review(brewery_id):
    """ shows a review form and handles a user review for particular brewery """

    if not g.user:
        flash("Access unauthorized. Please create a profile in order to leave a review.", "danger")
        return redirect("/")

    form = ReviewForm()
    form.rating.choices = rating_list()  

    try: 
        response = requests.get(f'{BASE_URL}/{brewery_id}')
        if response.status_code == 200:
            brewery = response.json()

    except Exception as e:
        print(e)
        return '<p>error</p>'

    if form.validate_on_submit():
        existing_brewery = Brewery.query.filter_by(api_id=brewery_id).first()
        if not existing_brewery:
            new_brewery = Brewery(
                            name=brewery['name'], 
                            brewery_type=brewery['brewery_type'], 
                            address=brewery['address_1'], 
                            city=brewery['city'], 
                            state_province=brewery['state_province'], 
                            postal_code=brewery['postal_code'], 
                            country=brewery['country'], 
                            phone=brewery['phone'], 
                            url=brewery['website_url'],
                            api_id=brewery['id'])
            db.session.add(new_brewery)
            db.session.commit()
            existing_id = new_brewery.id

        else: 
            existing_id = existing_brewery.id

        user = User.query.get_or_404(g.user.id)
        review = Review(rating=form.rating.data,
                        description=form.description.data,
                        brewery_id=existing_id,
                        user_id=g.user.id)
        db.session.add(review)
        db.session.commit()
        return redirect(f'/breweries/{brewery_id}')

    return render_template('review-form.html', form=form)