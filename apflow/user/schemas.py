from marshmallow import Schema, fields, ValidationError, validates


class UserSchema(Schema):
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password= fields.String(required=True, load_only=True)



class RoleSchema(Schema):
    name = fields.String(required=True)
    description = fields.String(required=True)
