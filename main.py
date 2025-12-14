from core.general import *

from lib.init import url, env

from flask import Flask, render_template
from flask_cors import CORS

from pages.test import app as test
from pages.model import app as model

app = Flask(__name__)
from pages.game_adapter import app as game_adapter
app.register_blueprint(game_adapter)
CORS(app)
# cors = CORS(app, resources={r"/*": {"origins": "domains"}})

app.register_blueprint(test)
app.register_blueprint(model)

@app.route('/')
def hello():
    return 'ouob<script> location.href=\'1\' </script>'

if __name__ == '__main__':
    if env('debug'): app.debug = True;
    app.run()
    quit()

