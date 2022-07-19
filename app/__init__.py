import os
import mongoengine

from flask import Flask
from app.config import Config, TestConfig
from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__)
    app.debug = True
    phase = os.environ.get('PHASE', 'local').lower()

    if test_config != None:
        app.config.from_object('app.config.TestConfig')
        mongoengine.connect("test", host=TestConfig.MONGO_URI)
    else:
        app.config.from_object('app.config.Config')
        mongoengine.connect("test", host=Config.MONGO_URI)
    CORS(app)

    from app.utils.viewhandler import register_api

    register_api(app)

    # app.config.update({
    #     'APISPEC_SPEC': APISpec(
    #         title="Title",
    #         version="1.0.0",
    #         openapi_version="3.0.2",
    #         plugins=[MarshmallowPlugin()],
    #     ),
    #     'APISPEC_SWAGGER_URL': '/swagger-json',
    #     'APISPEC_SWAGGER_UI_URL' : '/swagger/'
    # })

    return app
