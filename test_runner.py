import unittest
from test_brewery_model import BreweryModelTestCase

# Create a TestSuite
test_suite = unittest.TestSuite()

# Add your test class to the TestSuite
test_suite.addTest(unittest.makeSuite(BreweryModelTestCase))

# Run the tests
runner = unittest.TextTestRunner()
runner.run(test_suite)
