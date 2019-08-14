import json
import logging
import requests
from flask import render_template, request, Response
from flask.views import MethodView
from flask import Response
from initialization_package import app
from requests import exceptions
from werkzeug.exceptions import BadRequest


class Health(MethodView):
    """TBD
    """

    def get(self):
        """
        To be done
        :return:
        """

        #default_message = "NotReady"
        # Get the URL for the game modes
        logging.debug("Getting cowbull_modes_url from config:")
        cowbull_url = app.config.get('cowbull_modes_url', None)
        if cowbull_url is None:
            return Response(
                response=json.dumps(default_message),
                mimetype="application/json",
                status=500
            )
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
            return Response(
                response=json.dumps(error_message),
                mimetype="application/json",
                status=500
            )
        except Exception as e:
            logging.debug("Exception: {}".format(str(re)))
            error_message = "Game is unavailable. The server returned " \
                            "an error: {}.".format(str(re))
            return Response(
                response=json.dumps(error_message),
                mimetype="application/json",
                status=500
            )

        # Check the return status from the request. If it's not 200 (or any
        # other code we expected), return the error page.
        logging.debug("Checking return status from HTTP request")
        if r is None:
            logging.debug("Exception: r is None!")
            error_message = "The game is unavailable: this is unexpected."
            return Response(
                response=json.dumps(error_message),
                mimetype="application/json",
                status=500
            )

        # If the return status is anything other than 200 (ok), report an error
        # and return the error page.
        if r.status_code != 200:
            logging.debug("The HTTP request returned: {}".format(str(r.status_code)))
            error_message = "Game is unavailable. Status code {}".format(r.status_code)
            return Response(
                response=json.dumps(error_message),
                mimetype="application/json",
                status=r.status_code
            )

        return Response(
            response=json.dumps("Ready - Game server {} available".format(cowbull_url)),
            mimetype="application/json",
            status=200
        )
