import os
from flask import Flask, render_template, request, flash, redirect, url_for
import socket
import config
from datetime import timedelta

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)
print(IPAddr + "/pseudoID/generate")


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

    return app
