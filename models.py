""" SQLAlchemy models for HoppyHour """

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """ connects database to provided flask app """
    db.app = app
    db.init_app(app)
    

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

    def __repr__(self):
        return f'<Brewery {self.name} {self.brewery_type}>'

class Review(db.Model):
    """ Review model """

    id = db.Column(db.Integer,
                           primary_key=True)

    rating = db.Column(db.Integer)

    description = db.Column(db.Text)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id', ondelete='cascade'))

    brewery_id = db.Column(db.Integer,
                        db.ForeignKey('breweries.id', ondelete='cascade')) 