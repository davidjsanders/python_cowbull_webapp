import io
import logging
import os
import unittest
from unittest import TestCase

class TestApp(TestCase):
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
        self.default_modes_url = self.app.application.config['cowbull_modes_url']

    def tearDown(self):
        pass

    # Expect the game to fail in unit test. Cowbull server should NOT be running
    def test_no_game(self):
        self.app.application.config['cowbull_modes_url'] = self.default_modes_url
        response = self.app.get('/', follow_redirects=True)
        response_expected = "Game is unavailable"
        self.assertTrue(response_expected in str(response.get_data()))

    def test_health_notready(self):
        self.app.application.config['cowbull_modes_url'] = self.default_modes_url
        response = self.app.get('/health', follow_redirects=True)
        response_expected = "Game is unavailable"
        self.assertTrue(response_expected in str(response.get_data()))

    def test_bad_cowbull_url(self):
        with self.assertRaises(ValueError):
            self.app.application.config['cowbull_modes_url'] = None
            self.app.get('/', follow_redirects=True)
        self.app.application.config['cowbull_modes_url'] = self.default_modes_url

    