from marshmallow import Schema, fields


class CreateUrlInputSchema(Schema):
    full_url = fields.URL(required=True)
    shortcode = fields.String(required=False)
