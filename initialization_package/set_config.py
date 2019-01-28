import logging
import os


def set_config(app=None):
    if app is None:
        raise ValueError("APP is undefined!!")

    #
    # Expected OS Env Vars (lower case):
    # LOGGING_FORMAT --> Python logging fmt     !! Default: "%(asctime)s %(levelname)s: %(message)s"
    # COWBULL_SERVER --> server_url             !! Note NO TRAILING /
    # COWBULL_PORT   --> 80                     !! Note integer
    # FLASK_HOST     --> 0.0.0.0                !! Only if using Flask to serve
    # FLASK_PORT     --> 5000                   !! "    "    "    "    "    "

    #
    # Set the configuration for logging
    #
    logging.basic_config(
        level=int(os.getenv(
            "logging_level",
            os.getenv(
                "LOGGING_LEVEL",
                logging.DEBUG
            )
        )),
        format=os.getenv(
            "logging_format",
            os.getenv(
                "LOGGING_FORMAT",
                "%(asctime)s %(levelname)s: %(message)s"
            )
        )
    )

    #
    # Set the protocol for http(s).
    #
    logging.debug("Setting COWBULL_PROTOCOL")
    cowbull_protocol = os.getenv(
        "cowbull_protocol",
        os.getenv(
            "COWBULL_PROTOCOL",
            "http"
        )
    )
    app.config["cowbull_protocol"] = cowbull_protocol
    logging.debug("Setting COWBULL_PROTOCOL --> {}".format(app.config["cowbull_protocol"]))

    #
    # Set the server where the CowBull game is being accessed.
    #
    logging.debug("Setting COWBULL_SERVER")
    cowbull_server = os.getenv(
        "cowbull_server",
        os.getenv(
            "COWBULL_SERVER",
            "localhost"
        )
    )
    app.config["cowbull_server"] = cowbull_server
    logging.debug("Setting COWBULL_SERVER --> {}".format(app.config["cowbull_server"]))

    #
    # Set the port the CowBull game server is listening on.
    #
    logging.debug("Setting COWBULL_PORT")
    cowbull_port = os.getenv(
        "cowbull_port",
        os.getenv(
            "COWBULL_PORT",
            5000
        )
    )
    app.config["cowbull_port"] = cowbull_port
    logging.debug("Setting COWBULL_PORT --> {}".format(app.config["cowbull_port"]))

    #
    # Set the version of the game the CowBull server expects
    #
    logging.debug("Setting COWBULL_VERSION")
    cowbull_version = os.getenv(
        "cowbull_version",
        os.getenv(
            "COWBULL_VERSION",
            "v1"
        )
    )
    app.config["cowbull_version"] = cowbull_version
    logging.debug("Setting COWBULL_VERSION --> {}".format(app.config["cowbull_version"]))

    #
    # Set the full URL for the server
    #
    logging.debug("Setting COWBULL_URL")
    app.config["cowbull_url"] = "{}://{}:{}/{}".format(
        app.config["cowbull_protocol"],
        app.config["cowbull_server"],
        app.config["cowbull_port"],
        app.config["cowbull_version"]
    )
    logging.debug("Setting COWBULL_URL --> {}".format(app.config["cowbull_url"]))

    #
    # Set the full URL for getting the modes from the game server
    #
    logging.debug("Setting COWBULL_MODES_URL")
    app.config["cowbull_modes_url"] = "{}/modes".format(app.config["cowbull_url"])
    logging.debug("Setting COWBULL_MODES_URL --> {}".format(app.config["cowbull_modes_url"]))

    #
    # Set the full URL for playing the game
    #
    logging.debug("Setting COWBULL_GAME_URL")
    app.config["cowbull_game_url"] = "{}/game".format(app.config["cowbull_url"])
    logging.debug("Setting COWBULL_GAME_URL --> {}".format(app.config["cowbull_game_url"]))

    #
    # Set the environment
    #
    logging.debug("Setting ENVIRONMENT")
    environment = os.getenv(
        "cowbull_environment",
        os.getenv(
            "COWBULL_ENVIRONMENT",
            "dev"
        )
    )
    app.config["environment"] = environment
    logging.debug("Setting ENVIRONMENT --> {}".format(app.config["environment"]))

    #
    # Set the navbar colour
    #
    logging.debug("Setting NAVBAR_COLOUR")
    environment = os.getenv(
        "navbar_colour",
        os.getenv(
            "NAVBAR_COLOUR",
            "bg-primary"
        )
    )
    app.config["navbar_colour"] = environment
    logging.debug("Setting NAVBAR_COLOUR --> {}".format(app.config["navbar_colour"]))


    #
    # Set the build number
    #
    logging.debug("Setting BUILD_NUMBER")
    build_number = os.getenv(
        "build_number",
        os.getenv(
            "BUILD_NUMBER",
            "unknown"
        )
    )
    app.config["build_number"] = build_number
    logging.debug("Setting build_number --> {}".format(app.config["build_number"]))


    #
    # For debug only or when using Flask's built-in server. This variable sets
    # the host that Flask will listen on, e.g. 127.0.0.1, or 0.0.0.0.
    #
    logging.debug("Setting FLASK_HOST")
    app.config["FLASK_HOST"] = os.getenv(
        "flask_host",
        os.getenv(
            "FLASK_HOST",
            "0.0.0.0"
        )
    )

    #
    # For debug only or when using Flask's built-in server. This variable sets
    # the port that Flask will listen on, e.g. 5000, 5001, 8001, etc.
    #
    logging.debug("Setting FLASK_PORT")
    try:
        app.config["FLASK_PORT"] = int(os.getenv(
            "flask_port",
            os.getenv(
                "FLASK_PORT",
                8001
            )
        ))
    except ValueError:
        app.config["FLASK_PORT"] = 8001

    #
    # Dump the env vars to the log
    #
    logging.debug("COWBULL_PROTOCOL  : {}".format(app.config["cowbull_protocol"]))
    logging.debug("COWBULL_SERVER    : {}".format(app.config["cowbull_server"]))
    logging.debug("COWBULL_PORT      : {}".format(app.config["cowbull_port"]))
    logging.debug("COWBULL_VERSION   : {}".format(app.config["cowbull_version"]))
    logging.debug("COWBULL_URL       : {}".format(app.config["cowbull_url"]))
    logging.debug("COWBULL_MODES_URL : {}".format(app.config["cowbull_modes_url"]))
    logging.debug("COWBULL_GAME_URL  : {}".format(app.config["cowbull_game_url"]))
    logging.debug("NAVBAR_COLOR      : {}".format(app.config["navbar_colour"]))
    logging.debug("ENVIRONMENT       : {}".format(app.config["environment"]))
    logging.debug("FLASK_HOST        : {}".format(app.config["FLASK_HOST"]))
    logging.debug("FLASK_PORT        : {}".format(app.config["FLASK_PORT"]))
