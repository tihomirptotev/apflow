from marshmallow import Schema, fields, ValidationError, validates
from sqlalchemy.orm.exc import NoResultFound
from .models import User


class UserSchema(Schema):
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password= fields.String(required=True, load_only=True)
    url = fields.Url(dump_only=True)
    dbsession = None

    @validates('username')
    def validates_username(self, value):
        try:
            obj = self.dbsession.query(User).filter(
                User.username==value).first()
            if obj:
                raise ValidationError(
                    f'User with username: {value} already exsts.')
        except NoResultFound:
            pass

    @validates('email')
    def validates_email(self, value):
        try:
            obj = self.dbsession.query(User).filter(
                User.email == value).first()
            if obj:
                raise ValidationError(
                    f'User with email: {value} already exsts.')
        except NoResultFound:
            pass


class RoleSchema(Schema):
    name = fields.String(required=True)
    description = fields.String(required=True)
