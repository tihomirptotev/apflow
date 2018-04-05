from marshmallow import Schema, fields, ValidationError, validates, validate
from sqlalchemy.orm.exc import NoResultFound
from apflow.schemas.base_schema import BaseSchema
from .models import User



class UserSchema(BaseSchema):
    class Meta:
        fields = ('id', 'username', 'email')


class UserSignupSchema(Schema):
    username = fields.String(required=True,
                             validate=validate.Length(min=3, max=255))
    email = fields.Email(required=True)
    password= fields.String(required=True,
                            validate=validate.Length(min=8, max=128))

    @validates('username')
    def ensure_unique_username(self, value):
        user = User.get_by_identity(value, self.context['dbsession'])
        if user:
            raise ValidationError(f'{value} already exists.')

    @validates('email')
    def ensure_unique_email(self, value):
        user = User.get_by_identity(value, self.context['dbsession'])
        if user:
            raise ValidationError(f'{value} already exists.')


class UserSigninSchema(Schema):
    identity = fields.String(required=True,
                             validate=validate.Length(min=3, max=255))
    password = fields.String(required=True,
                             validate=validate.Length(min=8, max=128))


class RoleSchema(Schema):
    name = fields.String(required=True)
    description = fields.String(required=True)
