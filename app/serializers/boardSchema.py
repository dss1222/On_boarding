from marshmallow import fields, Schema, post_load

from app.Model import *


class BoardCreateSchema(Schema):
    name = fields.Str(required=True)


class BoardSchema(Schema):
    id = fields.Str()
    name = fields.Str()
