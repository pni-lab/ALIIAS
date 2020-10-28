import os
from flask import Flask, redirect, url_for
import sys
sys.path.append('/..')
from pseudoID import config

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import pseudonymize
    app.register_blueprint(pseudonymize.bp)

    if pseudonymize.handler.no_dongle:
        @app.route('/')
        def start():
            return redirect(url_for('pseudoID.nokey'))
    else:
        @app.route('/')
        def start():
            return redirect(url_for('pseudoID.login'))

    return app

from ._version import get_versions
__version__ = get_versions()['version']
del get_versions
