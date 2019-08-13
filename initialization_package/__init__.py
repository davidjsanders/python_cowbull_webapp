from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

#
# D Sanders, 12 Aug 2019 - Change static_path -> static_url_path
#
app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static/',
    static_url_path='/static'
)

app.wsgi_app = ProxyFix(app.wsgi_app)
