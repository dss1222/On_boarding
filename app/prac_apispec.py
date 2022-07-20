import json
from flask import Flask
from flask_classful import FlaskView
from flask_classful_apispec import APISpec
from marshmallow import Schema, fields

app = Flask(__name__)

app.config["DOC_TITLE"] = "Swagger petstore"
app.config["DOC_VERSION"] = "0.1.1"
app.config["DOC_OPEN_API_VERSION"] = "3.0.2"

spec = APISpec(app)

pets = [
    {'id': 0, 'name': 'Kitty', 'category': 'cat'},
    {'id': 1, 'name': 'Coco', 'category': 'dog'}
]


class PetSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    category = fields.String()


class PetView(FlaskView):
    def index(self):
        """A pet api endpoint.
        ---
        description: Get a list of pets
        responses:
          200:
            schema: PetSchema
        """
        return PetSchema(many=True).dumps(pets)


PetView.register(app)

with app.test_request_context():
    spec.paths(PetView, app)
print(json.dumps(spec.to_dict(), indent=2))

if __name__ == "__main__":
    app.run()
