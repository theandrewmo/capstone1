""" Review model tests """

# run these tests like:
#
# python -m unittest test_review_model.py

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Brewery, Review

os.environ['DATABASE_URL'] = "postgresql:///hoppyhour-test"

from app import app

db.create_all()

class ReviewModelTestCase(TestCase):
    """ Test review model """

    def setUp(self):
        """ Create test client, add sample data """

        db.drop_all()
        db.create_all()

        u1 = User.signup('testuser5', 'testuser5@test.com', 'testuser5', 'san diego', 'California', '91911', 'micro')
        b1 = Brewery(name='testbrewery',
                brewery_type='nano',
                address='testaddress',
                city='phoenix',
                state_province='Arizona',
                postal_code='85001',
                country='United States',
                phone='888888888',
                url='www.testbrewery.com',
                api_id=''
                )

        uid1 = 5555
        u1.id = uid1
        b1id = 2222
        b1.id = b1id
        db.session.add(b1)
        db.session.commit()

        u1 = User.query.get(uid1)
        b1 = Brewery.query.get(b1id)

        self.u1 = u1
        self.uid1 = uid1

        self.b1 = b1
        self.b1id = b1id
                
        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_review_model(self):
        """ Does basic model work? """

        review = Review(rating=5,
                description='test_description',
                timestamp=None,
                user_id=5555,
                brewery_id=2222
                )
        
        db.session.add(review)
        db.session.commit()

        self.assertEqual(review.description, 'test_description')

  