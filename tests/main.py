import unittest
import logging
from test_init import TestFundamentals

if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='unittest-reports'))
