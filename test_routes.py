""" Routes tests """

# run these tests like:
#
# python -m unittest test_routes.py

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Brewery, Review

os.environ['DATABASE_URL'] = "postgresql:///hoppyhour-test"

from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class RoutesTestCase(TestCase):
    """ Test routes """

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
    
    def test_index(self):
        """ Does index route work """

        with self.client as c:
            resp = c.get('/')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('HoppyHour', str(resp.data))

        with self.client as c:
            form_data =  {'term':'dog',
                          'search_type':''}
            resp = c.post('/')