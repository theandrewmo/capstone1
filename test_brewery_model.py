""" Brewery model tests """

# run these tests like:
#
# python -m unittest test_brewery_model.py

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Brewery, Review

os.environ['DATABASE_URL'] = "postgresql:///hoppyhour-test"

from app import app

db.create_all()

class BreweryModelTestCase(TestCase):
    """ Test brewery model """

    def setUp(self):
        """ Create test client, add sample data """

        db.drop_all()
        db.create_all()
        
        db.session.commit()
        
        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_brewery_model(self):
        """ Does basic model work? """

        b = Brewery(name='testbrewery',
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
        
        db.session.add(b)
        db.session.commit()

        self.assertEqual(b.name, 'testbrewery')

  