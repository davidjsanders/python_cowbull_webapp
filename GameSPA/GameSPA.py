import json
import logging
import requests
from flask import render_template, request, Response
from flask.views import MethodView
from initialization_package import app
from requests import exceptions
from werkzeug.exceptions import BadRequest


class GameSPA(MethodView):
    """GameSPA is the single page application 'engine' which serves the functionality
    required to play the game on a web browser. The MethodView supports three methods
    of interaction:

    - GET  : Initiates the SPA.
    - POST : Initiates a game from the game server.
    - PUT  : Allows a guess to be made against the game server.

    GameSPA is effectively the interface between the game and the game server:

    [---------]           [---------]           [-------------]
    [         ]           [         ]           [             ]
    [ Browser ]   <--->   [ GameSPA ]   <--->   [ Game Server ]
    [         ]           [         ]           [             ]
    [---------]           [---------]           [-------------]

    Why not allow the browser to talk directly to the game server? To abstract the
    game away from the user interface. Other 'front-ends' to the game include text,
    mobile apps, chat bots, etc., and go through similar interfaces. This enables
    the game to be modified once and all changes to be picked up directly from the
    server.
    """

    @staticmethod
    def _fetch_modes():
        """
        To be done
        :return:
        """

        # Get the URL for the game modes
        logging.debug("Getting cowbull_modes_url from config:")
        cowbull_url = app.config.get('cowbull_modes_url', None)
        if cowbull_url is None:
            raise ValueError("CowBull URL is Null!")
        logging.debug("Getting cowbull_modes_url from config: {}".format(cowbull_url))

        # Try and connect to the game server to get the available modes. If an exception
        # is raised, return the error page.
        try:
            logging.debug("Connecting [GET] to {}".format(cowbull_url))
            r = requests.get(url=cowbull_url)
        except exceptions.ConnectionError as re:
            logging.debug("Exception: {}".format(str(re)))
            error_message = "Game is unavailable. The server returned " \
                            "an error: {}.".format(str(re))
            return_state = False
            return_data = render_template(
                "error.html",
                error_message=error_message
            )
            return return_state, return_data
        except Exception as e:
            logging.debug("Exception: {}".format(repr(e)))
            error_message = "The game is unavailable: {}.".format(repr(e))
            return_state = False
            return_data = render_template(
                "error.html",
                error_message=error_message
            )
            return return_state, return_data

        # Check the return status from the request. If it's not 200 (or any
        # other code we expected), return the error page.
        logging.debug("Checking return status from HTTP request")
        if r is None:
            logging.debug("Exception: r is None!")
            error_message = "The game is unavailable: this is unexpected."
            return_state = False
            return_data = render_template(
                "error.html",
                error_message=error_message
            )
            return return_state, return_data

        # If the return status is anything other than 200 (ok), report an error
        # and return the error page.
        if r.status_code != 200:
            logging.debug("The HTTP request returned: {}".format(str(r.status_code)))
            error_message = "Game is unavailable. Status code {}".format(r.status_code)
            return_state = False
            return_data = render_template(
                "error.html",
                error_message=error_message
            )
            return return_state, return_data

        #
        # Get the modes from the JSON returned. The game server specification states the
        # schema to expect and a to do item will validate the returned JSON. The modes
        # are stored in modes_table and in the app.config for later access. When the
        # value is extracted from app.config, it must be checked for staleness (i.e.
        # the value will be []) and refreshed with a call to this method.
        #
        logging.debug("Extracting JSON from the GET request")
        try:
            modes_data = r.json()
            logging.debug("JSON extracted is: {}".format(modes_data))
        except Exception as e: # Blanket catch-all as this should never occur.
            logging.debug("Exception: {}".format(repr(e)))
            error_message = "The game is unavailable: {}.".format(repr(e))
            return_state = False
            return_data = render_template(
                "error.html",
                error_message=error_message
            )
            return return_state, return_data

        return_state = True
        return_data = modes_data

        app.config["modes_data"] = modes_data

        return return_state, return_data

    def get(self):
        """get provides the initial response to the browser request, gets the modes
        supported by the game server, and presents the initial page UI to the user.

        Configuration for the SPA is provided in initialization_package.set_config()

        If the game server is unresponsive (for any reason), get will return a rendered
        error template; otherwise, get returns index.html.
        """

        #
        # Get the game modes for the server providing this game. If the call does
        # not set valid to True, then the modes_table variable will be set to a
        # rendered error.html page and should be returned to the caller.
        #
        valid, modes_data = self._fetch_modes()
        if not valid:
            return modes_data

        modes_table = modes_data["modes"]
        modes_instructions = modes_data["instructions"]
        modes_notes = modes_data["notes"]

        # Render the index.html template
        logging.debug("Rendering index.html template.")
        return_template = render_template(
            "index.html",
            digits=0,
            guesses=0,
            modes_table=modes_table,
            modes_instructions=modes_instructions,
            modes_notes=modes_notes,
            navbar_colour=app.config.get('navbar_colour', 'bg-primary'),
            build_number=app.config.get('build_number', 'unknown'),
            environment=app.config.get('environment', 'dev'),
            gameserver=app.config.get('cowbull_url', None)
        )

        # Return the template
        logging.debug("Returning rendered index.html template")
        return return_template

    def post(self):
        """post provides the response to the browser request when a user chooses a
        game mode and starts a new game. It renders playgame.html and returns an
        appropriately sized game board. The mode is passed as a form parameter.

        Configuration for the SPA is provided in initialization_package.set_config()

        If the game server is unresponsive (for any reason), get will return a rendered
        error template; otherwise, get returns index.html.
        """

        # Get the mode from the form and default to normal if it is not present for
        # some reason.
        mode = request.form.get("mode", "normal")

        # Get the modes_table from the app config; if it is stale ([]), then it will
        # be refreshed using _fetch_modes.
        modes_data = app.config.get("modes_data", None)
        if modes_data is None:
            valid, modes_data = self._fetch_modes()
            if not valid:
                return modes_data

        modes_table = modes_data["modes"]

        # Set the request response to None so it can be caught later.
        r = None

        # Get the game URL and set the mode.
        logging.debug("Getting cowbull_game_url from config:")
        cowbull_url = app.config.get("cowbull_game_url")+"?mode={}".format(mode)
        if cowbull_url is None:
            raise ValueError("CowBull URL is Null!")
        logging.debug("Getting cowbull_game_url from config: {}".format(cowbull_url))

        # Connect to the game server and get a new game.
        try:
            logging.debug("Getting game from {}".format(cowbull_url))
            r = requests.get(url=cowbull_url)
        except exceptions.ConnectionError as re:
            error_message = "Game is unavailable: {}.".format(str(re))
            return render_template(
                "error.html",
                error_message="For some reason, it hasn't been possible "
                              "to get a game. The raw return was: {}".format(str(re))
            )

        # Check the return status from the request. If it's not 200 (or any
        # other code we expected) or it's None, return the error page.
        if r is None:
            logging.debug("The game request failed! {}".format(r.raw))
            return render_template(
                "error.html",
                error_message="For some reason, it hasn't been possible "
                              "to get a game. The raw return was: {}".format(r.raw)
            )

        if r.status_code != 200:
            logging.debug(
                "The game request failed! Status code = {}, raw result = {}".format(r.status_code, r.text)
            )
            return render_template(
                "error.html",
                error_message="For some reason, it hasn't been possible "
                              "to get a game. The status code was: {}"
                .format(r.status_code)
            )

        logging.debug("The game was fetched successfully: {}".format(r.status_code))

        try:
            game_object = r.json()
            logging.debug("JSON extracted: {}".format(game_object))
        except Exception as e:
            logging.debug(
                "The game request failed with an exception: {}".format(repr(e))
            )
            return render_template(
                "error.html",
                error_message="For some reason, it hasn't been possible "
                              "to get a game. The exception was: {}"
                .format(repr(e))
            )

        return_template = render_template(
            "playgame.html",
            digits=game_object.get("digits", None),
            guesses=game_object.get("guesses", None),
            key=game_object.get("key", None),
            environment=app.config.get('environment', 'dev'),
            navbar_colour=app.config.get('navbar_colour', 'bg-primary'),
            build_number=app.config.get('build_number', 'unknown'),
            served_by=game_object.get("served-by", "None"),
            modes_table=modes_table,
            mode_name=game_object.get("mode", ""),
            mode_help=game_object.get("help-text", ""),
            mode_instructions=game_object.get("instruction-text", "")
        )

        return return_template

    def put(self):
        # Check circuit breaker

        #
        # Get the JSON from the request
        #
        try:
            logging.debug('Attempting to load JSON from PUT request')
            json_dict = request.get_json()
            if not json_dict:
                raise BadRequest("There was no JSON contained in the PUT request!")

            logging.debug('Loaded JSON. Returned: {}'.format(json_dict))

            key = json_dict.get('key', None)
            digits = json_dict.get('digits', [])

            if key is None or digits == []:
                raise BadRequest(
                    description="The JSON is malformed; either key is None or there are no digits."
                )
        except BadRequest as br:
            logging.debug('A BadRequest exception raised while loading JSON: {}'.format(str(br)))
            response = Response(
                response=json.dumps({
                    "status": 400,
                    "message": "Failed to respond to guess.",
                    "exception": str(br)
                }),
                status=400,
                mimetype="application/json"
            )
            return response

        # Get the game URL.
        logging.debug("Getting cowbull_game_url from config:")
        cowbull_url = app.config.get("cowbull_game_url")
        if cowbull_url is None:
            raise ValueError("CowBull URL is Null!")
        logging.debug("Getting cowbull_game_url from config: {}".format(cowbull_url))

        # Issue a post request to the game server with the data provided
        r = None
        try:
            headers = {"Content-type": "application/json"}
            logging.debug(
                "Issuing game POST request. Headers: {}; Data: {}".format(
                    headers,
                    json_dict
                )
            )
            r = requests.post(url=cowbull_url, data=json.dumps(json_dict), headers=headers)
        except Exception as e:
            logging.debug("Exception raised: {}".format(repr(e)))
            response = Response(
                response=json.dumps({
                    "status": 500,
                    "message": "Failed to respond to guess.",
                    "exception": repr(e)
                }),
                status=500,
                mimetype="application/json"
            )
            return response

        # Check the return status from the request. If it's not 200 (or any
        # other code we expected), return the error page.
        logging.debug("XHR Request status: {}".format(r.status_code))

        #
        # A status code of 200 (ok) or 400 (client error) is okay and will return
        # the response information as part of the JSON from the game server;
        # anything else should be reported as an error.
        #
        if r.status_code not in (200, 400):
            logging.debug("Request failed with status {}; raw: {}".format(r.status_code, r.text))
            response = Response(
                response=json.dumps({
                    "status": 500,
                    "message": "Failed to respond to guess with status code: {}",
                    "exception": str(r.status_code)
                }),
                status=500,
                mimetype="application/json"
            )
            return response

        # Extract the JSON from the response and return it to the caller.
        try:
            logging.debug("Extracting JSON from response.")
            json_response = r.json()
            if not json_response:
                raise BadRequest("The JSON response was None!")
        except Exception as e:
            logging.debug("JSON extraction failed: {}".format(repr(e)))
            response = Response(
                response=json.dumps({
                    "status": 500,
                    "message": "Failed to respond to guess. An exception was raised: {}",
                    "exception": repr(e)
                }),
                status=500,
                mimetype="application/json"
            )
            return response

        logging.debug("Returning response to caller: {}".format(json_response))
        return Response(
            response=json.dumps(json_response),
            status=r.status_code,
            mimetype="application/json"
        )
