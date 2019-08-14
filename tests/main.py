import logging
import unittest
from test_App import Test_App
from test_Methods import Test_Methods

if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='unittest-reports'))
