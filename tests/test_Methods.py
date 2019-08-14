import io
import logging
import os
import unittest
from app import app
from GameSPA.GameSPA import GameSPA
from initialization_package.set_config import set_config
from unittest import TestCase

class Test_Methods(TestCase):
    def setUp(self):
        # Setup the environment to ensure any running cowbull
        # game server is ignored.
        os.environ['COWBULL_SERVER'] = '0'
        os.environ['COWBULL_PORT'] = '0'

        # Import the app and set the config.
        from app import app
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        self.app = app.test_client()

    def tearDown(self):
        pass

    def test_set_config(self):
        # Note: PASS the real app not the test app
        get = set_config(self.app.application)

    def test_set_config_value_error(self):
        with self.assertRaises(ValueError):
            get = set_config()

    # Expect the game to fail in unit test. Cowbull server should NOT be running
    # def test_no_game(self):
    #     response = self.app.get('/', follow_redirects=True)
    #     response_expected = "Game is unavailable"
    #     self.assertTrue(response_expected in str(response.get_data()))

    if __name__ == "__main__":
        unittest.main()
