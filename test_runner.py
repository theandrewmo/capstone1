import unittest
from test_user_model import UserModelTestCase
from test_brewery_model import BreweryModelTestCase
from test_review_model import ReviewModelTestCase
from test_photo_model import PhotoModelTestCase
from test_routes import RoutesTestCase

# Create a TestSuite
test_suite = unittest.TestSuite()

# Add your test class to the TestSuite
test_suite.addTest(unittest.makeSuite(UserModelTestCase))
test_suite.addTest(unittest.makeSuite(BreweryModelTestCase))
test_suite.addTest(unittest.makeSuite(ReviewModelTestCase))
# test_suite.addTest(unittest.makeSuite(PhotoModelTestCase))
test_suite.addTest(unittest.makeSuite(RoutesTestCase))


# Run the tests
runner = unittest.TextTestRunner()
runner.run(test_suite)
