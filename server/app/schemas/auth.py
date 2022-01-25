from marshmallow import Schema, fields


class AuthInputSchema(Schema):
    password = fields.Str(required=True)