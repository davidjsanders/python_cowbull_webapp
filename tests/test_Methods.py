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

    def test_set_config_custom_config(self):
        # Note: PASS the real app not the test app
        os.environ['COWBULL_PROTOCOL'] = "https"
        os.environ['COWBULL_SERVER'] = "foobar"
        os.environ['COWBULL_PORT'] = "8"
        os.environ['COWBULL_VERSION'] = "v2"
        os.environ['COWBULL_ENVIRONMENT'] = "UnitTest"
        os.environ['NAVBAR_COLOUR'] = "BLUE"
        os.environ['BUILD_NUMBER'] = "1.2.3.4"
        os.environ['FLASK_PORT'] = "80"
        os.environ['FLASK_HOST'] = "4.3.2.1"
        get = set_config(self.app.application)
        self.assertEqual(self.app.application.config['cowbull_protocol'], "https")
        self.assertEqual(self.app.application.config['cowbull_server'], "foobar")
        self.assertEqual(self.app.application.config['cowbull_port'], "8")
        self.assertEqual(self.app.application.config['cowbull_version'], "v2")
        self.assertEqual(
            self.app.application.config['cowbull_url'], 
            "https://foobar:8/v2"
            )
        self.assertEqual(
            self.app.application.config['cowbull_modes_url'], 
            "https://foobar:8/v2/modes"
            )
        self.assertEqual(
            self.app.application.config['cowbull_game_url'], 
            "https://foobar:8/v2/game"
            )
        self.assertEqual(self.app.application.config['environment'], "UnitTest")
        self.assertEqual(self.app.application.config['navbar_colour'], "BLUE")
        self.assertEqual(self.app.application.config['build_number'], "1.2.3.4")
        self.assertEqual(self.app.application.config['FLASK_PORT'], 80)
        self.assertEqual(self.app.application.config['FLASK_HOST'], '4.3.2.1')

    def test_set_config_bad_port(self):
        # Note: PASS the real app not the test app
        os.environ['FLASK_PORT'] = "BADINT"
        get = set_config(self.app.application)
        self.assertEqual(self.app.application.config['FLASK_PORT'], 8001)

    def test_set_config_value_error(self):
        with self.assertRaises(ValueError):
            get = set_config()

    def test_health_notready(self):
        response = self.app.get('/health', follow_redirects=True)
        response_expected = "b'\"NotReady\"'"
        self.assertEquals(response_expected, str(response.get_data()))
        
    # Expect the game to fail in unit test. Cowbull server should NOT be running
    # def test_no_game(self):
    #     response = self.app.get('/', follow_redirects=True)
    #     response_expected = "Game is unavailable"
    #     self.assertTrue(response_expected in str(response.get_data()))
