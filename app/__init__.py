import os
import mongoengine

from flask import Flask
from app.config import Config, TestConfig
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__)
    if test_config != None:
        app.config.from_object('app.config.TestConfig')
        mongoengine.connect("test", host=TestConfig.MONGO_URI)
    else:
        app.config.from_object('app.config.Config')
        mongoengine.connect("test", host=Config.MONGO_URI)
    CORS(app)

    from app.utils.viewhandler import register_api

    register_api(app)

    return app
