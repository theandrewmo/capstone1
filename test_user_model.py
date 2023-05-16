""" User model tests """

# run these tests like:
#
# python -m unittest test_user_model.py

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Brewery, Review

os.environ['DATABASE_URL'] = "postgresql:///hoppyhour-test"

from app import app

db.create_all()

class UserModelTestCase(TestCase):
    """ Test user model """

    def setUp(self):
        """ Create test client, add sample data """

        db.drop_all()
        db.create_all()

        u1 = User.signup('testuser1', 'testuser1@test.com', 'testuser1', 'san diego', 'California', '91911', 'micro')
        u2 = User.signup('testuser2', 'testuser2@test.com', 'testuser2', 'beverly hills', 'California', '90210', 'nano')

        uid1 = 1111
        u1.id = uid1
        uid2 = 2222
        u2.id = uid2
        
        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2
        
        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res
    
    def test_user_model(self):
        """ Does basic model work? """

        u = User(username='tester',
                 email='tester@test.com',
                 password='tester',
                 city='phoenix',
                 state='Arizona',
                 postal_code='85001',
                 fav_type='brewpub'
                 )
        
        db.session.add(u)
        db.session.commit()

        self.assertEqual(u.username, 'tester')

    ### Signup Tests

    def test_valid_signup(self):
        u_test = User.signup('testuser3', 'testuser3@test.com', 'testuser3', 'new york', 'New York', '10001', 'regional')
        uid = 99999
        u_test.id = uid
        db.session.commit()

        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "testuser3")
        self.assertEqual(u_test.email, "testuser3@test.com")
        self.assertNotEqual(u_test.password, "testuser3")
        # Bcrypt strings should start with $2b$
        self.assertTrue(u_test.password.startswith("$2b$"))

    def test_invalid_username_signup(self):
        invalid = User.signup(None, "test@test.com", "password", None, None, None, None)
        uid = 123456789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()

    def test_invalid_email_signup(self):
        invalid = User.signup("testtest", None, "password", None, None, None, None)
        uid = 123789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    
    def test_invalid_password_signup(self):
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "email@email.com", "", None,  None, None, None)
        
        with self.assertRaises(ValueError) as context:
            User.signup("testtest", "email@email.com", None, None, None, None, None)

    ### Authentication Tests
    
    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username, "testuser1")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid1)
    
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "testuser1"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "badpassword"))