""" Routes tests """

# run these tests like:
#
# python -m unittest test_routes.py

import os
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Brewery, Review, generate_reset_token

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

    def test_signup(self):
        """ Does signup work """

        with self.client as c: 
            resp = c.get('/signup')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Join', str(resp.data))

        with self.client as c: 
            form_data = {'username': 'testuser1', 'password': 'testpassword', 'email': 'testuser1@test.com',
                         'city': 'San Diego', 'state': 'California', 'postal_code': '91911', 'fav_type': 'micro'}
            resp = c.post('/signup', data=form_data, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('successful', str(resp.data))

    def test_failed_signup(self):
        """ Ensures signup fails when incorrect data for user model, such as postal code with too many characters"""

        with self.client as c:
            form_data = {'username': 'testuser2', 'password': 'testpassword', 'email': 'testuser2@test.com',
                         'city': 'San Diego', 'state': 'California', 'postal_code': '91911999393939', 'fav_type': 'micro'}
            resp = c.post('/signup', data=form_data, follow_redirects=True)
            
            self.assertEqual(resp.status_code, 200)
            self.assertIn('signup failed', str(resp.data))

    def test_login(self):
        """ Ensures login works """

        with self.client as c:
            resp = c.get('/login')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Welcome', str(resp.data))

        with self.client as c: 
            form_data = {'username': 'testuser5', 'password': 'testuser5'}
            resp = c.post('/login', data=form_data, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('successful', str(resp.data))

    def test_failed_login(self):
        """ Ensures login fails accordingly when given incorrect password """

        with self.client as c: 
            form_data = {'username': 'testuser5', 'password': 'wrongpassword'}
            resp = c.post('/login', data=form_data, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('unsuccessful', str(resp.data))

    def test_logout(self):
        """ Ensures logout works """

        with self.client as c:
            resp = c.get('/logout', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Welcome', str(resp.data))   

    def test_edit(self):
        """ Does edit user work """    

        # return unauthorized message when user is not logged in

        with self.client as c:
            resp = c.get('/edit', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('unauthorized', str(resp.data))   

        # log user in

        with self.client as c:
            form_data = {'username': 'testuser5', 'password': 'testuser5'}
            resp = c.post('/login', data=form_data, follow_redirects=True)

        # ensures the edit is allowed when user is logged in and the information is updated correctly

        with self.client as c:
            form_data =  {'username': 'testuser5', 'password': 'testuser5', 'fav_type': 'nano'}
            resp = c.post('/edit', data=form_data, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('User profile updated successfully', str(resp.data))
        
            updated_user = User.query.filter_by(username='testuser5').first()
            self.assertIsNotNone(updated_user)
            self.assertEqual(updated_user.fav_type, 'nano')

    def test_forgot_password(self):
        """ Ensures forgot password works """

        with self.client as c:
            resp = c.get('/forgot_password', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Enter Email', str(resp.data))   

        with self.client as c:
            form_data =  {'email': 'testuser5@test.com'}
            resp = c.post('/forgot_password', data=form_data, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Password reset email sent successfully.', str(resp.data))
        
    def test_forgot_password_fail(self):
        # test error message when user not in database
        with self.client as c:
            form_data =  {'email': 'notindatabase@fake.com'}
            resp = c.post('/forgot_password', data=form_data, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('User not found', str(resp.data))

    def test_reset_password(self):
        """ Ensures reset password works """
        
        test_user = User.query.filter_by(email='testuser5@test.com').first()
        token = generate_reset_token(test_user)

        with self.client as c:
            resp = c.get('/reset_password/'+token, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Enter new password', str(resp.data))   

        with self.client as c:
            form_data =  {'new_password': 'newpassword', 'confirm_password': 'newpassword'}
            resp = c.post('/reset_password/'+token, data=form_data, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Password reset successfully.', str(resp.data))
        
        # test error message when passwords don't match
        with self.client as c:
            form_data =  {'new_password': 'newpassword', 'confirm_password': 'doesntmatch'}
            resp = c.post('/reset_password/'+token, data=form_data, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Passwords do not match.', str(resp.data))

        # test error message when token is not valid
        with self.client as c:
            token = 'invalid'
            form_data =  {'new_password': 'newpassword', 'confirm_password': 'doesntmatch'}
            resp = c.post('/reset_password/'+token, data=form_data, follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Invalid or expired token', str(resp.data))

    def test_brewery(self):
        """ Does brewery route work """

        # this route uses the API so first setup a brewery instance based on a real brewery in API

        with self.client as c:
            b2 = Brewery(name='(405) Brewing Co',
                brewery_type='nano',
                address='1716 Topeka St',
                city='Norman',
                state_province='Oklahoma',
                postal_code='73069',
                country='United States',
                phone='4058160490',
                url='http://www.405brewing.com',
                api_id='5128df48-79fc-4f0f-8b52-d06be54d0cec'
                )

            b2id = 9999
            b2.id = b2id
            db.session.add(b2)
            db.session.commit()

            resp = c.get('/breweries/5128df48-79fc-4f0f-8b52-d06be54d0cec')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('(405) Brewing Co', str(resp.data))
        
        # add a review for this brewery, and see if the review will show up for this brewery on the details page

            r1 = Review(rating=3, description='this is a test review', user_id=5555, brewery_id=9999)
            db.session.add(r1)
            db.session.commit()

            resp = c.get('/breweries/5128df48-79fc-4f0f-8b52-d06be54d0cec')

            self.assertEqual(resp.status_code, 200)
            self.assertIn('this is a test review', str(resp.data))

    def test_brewery_fail(self):
         """ Ensure brewery route fails with proper message when given an invalid brewery id """

         with self.client as c:
            resp = c.get('/breweries/1', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Brewery not found', str(resp.data))

    def test_review(self):
        """ Ensure review route works """

        # get 'unauthorized' message when not logged in

        with self.client as c:
            resp = c.get('/review/5128df48-79fc-4f0f-8b52-d06be54d0cec', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Access unauthorized', str(resp.data))

        # log in test user

        with self.client as c:
            form_data = {'username': 'testuser5', 'password': 'testuser5'}
            resp = c.post('/login', data=form_data, follow_redirects=True)

        # get form to submit a review now that user is logged in

        with self.client as c:
            resp = c.get('/review/5128df48-79fc-4f0f-8b52-d06be54d0cec', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Leave a Review', str(resp.data))  

        # check for proper message when brewery / review not found

        with self.client as c: 

            resp = c.get('/review/1', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Brewery not found', str(resp.data)) 
        
        # get message that this brewery has already been reviewed if user has already reviewed brewery

        with self.client as c:
            
            b2 = Brewery(name='(405) Brewing Co',
                brewery_type='nano',
                address='1716 Topeka St',
                city='Norman',
                state_province='Oklahoma',
                postal_code='73069',
                country='United States',
                phone='4058160490',
                url='http://www.405brewing.com',
                api_id='5128df48-79fc-4f0f-8b52-d06be54d0cec'
                )

            b2id = 9999
            b2.id = b2id
            db.session.add(b2)
            db.session.commit()

            r1 = Review(rating=3, description='this is a test review', user_id=5555, brewery_id=9999)
            db.session.add(r1)
            db.session.commit()

            resp = c.get('/review/5128df48-79fc-4f0f-8b52-d06be54d0cec', follow_redirects=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('You have already reviewed this brewery.', str(resp.data)) 
