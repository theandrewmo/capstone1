""" SQLAlchemy models for HoppyHour """

from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """ connects database to provided flask app """
    db.app = app
    db.init_app(app)

def states_list():
    return ["", "Alaska", "Alabama", "Arkansas", "American Samoa", "Arizona", 
            "California", "Colorado", "Connecticut", "District ", "of Columbia", 
            "Delaware", "Florida", "Georgia", "Guam", "Hawaii", "Iowa", "Idaho", 
            "Illinois", "Indiana", "Kansas", "Kentucky", "Louisiana", "Massachusetts", 
            "Maryland", "Maine", "Michigan", "Minnesota", "Missouri", "Mississippi", 
            "Montana", "North Carolina", "North Dakota", "Nebraska", "New Hampshire", 
            "New Jersey", "New Mexico", "Nevada", "New York", "Ohio", "Oklahoma", 
            "Oregon", "Pennsylvania", "Puerto Rico", "Rhode Island", "South Carolina", 
            "South Dakota", "Tennessee", "Texas", "Utah", "Virginia", "Virgin Islands", 
            "Vermont", "Washington", "Wisconsin", "West Virginia", "Wyoming"]

def type_list():
    return ['', 'micro', 'nano', 'regional', 'brewpub', 'large', 'planning',
            'bar', 'contract', 'proprietor']

def choice_list():
    return ['by keyword', 'by city', 'by distance', 'by name', 'by state', 'by type', 'get a random brewery']

def rating_list():
    return [5, 4, 3, 2, 1]

class User(db.Model):
    """ User model """

    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True)
    
    username = db.Column(db.Text,
                         nullable=False,
                         unique=True)

    email = db.Column(db.Text,
                      nullable=False,
                      unique=True)
    
    password = db.Column(db.Text,
                         nullable=False)
    
    city = db.Column(db.String(50))

    state = db.Column(db.String(50))

    postal_code = db.Column(db.String(10))

    fav_type = db.Column(db.String(30))

    def __repr__(self):
        return f'<User {self.username} {self.email}>'
    
    @classmethod
    def signup(cls, username, email, password, city, state, postal_code, fav_type):
        """ Sign up user. Hash password """
        
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            city=city,
            state=state,
            postal_code=postal_code,
            fav_type=fav_type
        )

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """ Authenticate user """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        
        return False
    
class UserLocation(db.Model):
    """ Location model """

    __tablename__ = 'user_location'

    id = db.Column(db.Integer,
                   primary_key=True)

    latitude = db.Column(db.String(50))

    longitude = db.Column(db.String(50))

    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.id', ondelete='CASCADE'))
    
    def __repr__(self):
        return f'<UserLocation user: {self.user_id}, lat: {self.latitude}, long: {self.longitude}>'
    

class Brewery(db.Model):
    """ Brewery model """

    __tablename__ = 'breweries'
    
    id = db.Column(db.Integer,
                   primary_key=True)
    
    name = db.Column(db.String(100),
                     nullable=False)
    
    brewery_type = db.Column(db.String(30))

    address = db.Column(db.String(100))

    city = db.Column(db.String(100))

    state_province = db.Column(db.String(100))

    postal_code = db.Column(db.String(10))
    
    country = db.Column(db.String(100))

    phone = db.Column(db.String(100))

    url = db.Column(db.Text)

    api_id = db.Column(db.String(100))

    def __repr__(self):
        return f'<Brewery {self.name} {self.brewery_type}>'

class Review(db.Model):
    """ Review model """

    __tablename__ = 'reviews'

    id = db.Column(db.Integer,
                           primary_key=True)

    rating = db.Column(db.Integer)

    description = db.Column(db.Text)

    timestamp = db.Column(db.DateTime,
                          nullable=False,
                          default=datetime.utcnow)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='CASCADE'))

    brewery_id = db.Column(db.Integer,
                        db.ForeignKey('breweries.id', ondelete='CASCADE'))

    brewery = db.relationship("Brewery", backref='review') 

    user = db.relationship("User", backref='review')

class Photo(db.Model):
    """ Photo model """

    __tablename__ = 'photos'

    id = db.Column(db.Integer,
                   primary_key=True)
    
    photo_url = db.Column(db.Text,
                          nullable=False)
    
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='CASCADE'))
    
    brewery_id = db.Column(db.Integer,
                        db.ForeignKey('breweries.id', ondelete='CASCADE'))
    
    review_id = db.Column(db.Integer,
                          db.ForeignKey('reviews.id', ondelete='CASCADE'))

    brewery = db.relationship("Brewery", backref='photos') 

    user = db.relationship("User", backref='photos')

    review = db.relationship("Review", backref='photos')