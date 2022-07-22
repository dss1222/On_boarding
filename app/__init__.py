import os
import mongoengine

from flask import Flask
from app.config import Config, TestConfig
from flask_cors import CORS

__version__ = "0.1.0"


def create_app(test_config=None):
    app = Flask(__name__, static_url_path='/static')
    app.debug = True

    app.config.from_object('app.config.Config')

    if test_config is not None:
        app.config.from_object('app.config.TestConfig')
        mongoengine.connect("test", host=TestConfig.MONGO_URI)
    else:
        app.config.from_object('app.config.Config')
        mongoengine.connect("test", host=Config.MONGO_URI)
    CORS(app)

    from app.utils.viewhandler import register_api

    register_api(app)

    return app
