import logging
import unittest
from test_App import TestApp
from test_Methods import TestMethods

if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='unittest-reports'))
