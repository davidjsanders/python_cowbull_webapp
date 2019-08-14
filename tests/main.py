import logging
import unittest
from test_GameSPA import Test_GameSPA

if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='unittest-reports'))
