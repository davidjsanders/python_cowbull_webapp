from GameSPA.GameSPA import GameSPA
from Health.Health import Health
from initialization_package import app
from initialization_package.set_config import set_config

# Set configuration from environment variables.
set_config(app=app)

# Add a game view. The game view is actually contained within a class
# based on a MethodView. See flask_controllers/GameController.py
game_view = GameSPA.as_view('Game')
app.add_url_rule(
    '/',
    view_func=game_view,
    methods=["GET", "POST", "PUT"]
)

# Add a health view. The health view is actually contained within a class
# based on a MethodView. See Health/Health.py
health_view = Health.as_view('Health')
app.add_url_rule(
    '/health',
    view_func=health_view,
    methods=["GET"]
)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

#
# The "__main__" code block typically only executes when run from
# the command line, e.g. python app.py. The app.run call is ignored
# when called from environments like GAE.
#
if __name__ == "__main__":
    app.run(
        host=app.config["FLASK_HOST"],
        port=app.config["FLASK_PORT"],
        debug=True
    )
