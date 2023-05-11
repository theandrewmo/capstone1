""" Seed database with sample data from CSV files"""

from app import db  
from models import User, Brewery, Review

db.drop_all()
db.create_all()

user1 = User.signup('hoppyguy21',
            'hoppy@hoppy.com',
            'hoppyguy',    
            'san francisco',
            'California',
            '94016',
            'micro')

user2 = User.signup('beerdude',
            'beer@beer.com',
            'beerdude',    
            'boulder',
            'Colorado',
            '80301',
            'brewpub')

db.session.commit()

