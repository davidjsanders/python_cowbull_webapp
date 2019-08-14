import io
import logging
import os
import unittest
from unittest import TestCase

class Test_App(TestCase):
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

    # Expect the game to fail in unit test. Cowbull server should NOT be running
    def test_no_game(self):
        response = self.app.get('/', follow_redirects=True)
        response_expected = "Game is unavailable"
        self.assertTrue(response_expected in str(response.get_data()))

    if __name__ == "__main__":
        unittest.main()
