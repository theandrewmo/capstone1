import unittest
from test_user_model import UserModelTestCase

# Create a TestSuite
test_suite = unittest.TestSuite()

# Add your test class to the TestSuite
test_suite.addTest(unittest.makeSuite(UserModelTestCase))

# Run the tests
runner = unittest.TextTestRunner()
runner.run(test_suite)
