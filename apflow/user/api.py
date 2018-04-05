from marshmallow.exceptions import ValidationError
from pyramid.response import Response
from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPNotFound
from pyramid.security import ALL_PERMISSIONS, Allow, Deny, Everyone, DENY_ALL, Authenticated
from sqlalchemy.orm import load_only
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from apflow.views.base_api import BaseApi
from .models import User, Role
from .schemas import UserSchema


@view_defaults(renderer='json')
class UserApi(BaseApi):

    __acl__ = [
        (Allow, 'admins', 'crud')
    ]

    class Meta:
        model_class = User
        schema = UserSchema(only=('id', 'username', 'email'))
        detail_route_name = 'user_view'

    @view_config(route_name='signup', request_method='POST')
    def signup(self):
        schema = UserSchema(only=('username', 'email', 'password'))
        schema.dbsession = self.request.dbsession
        try:
            data = schema.load(self.request.json_body)
            user = self.model(**data)
            user.save(self.request.dbsession)
            self.request.response.status_code = 201
            return dict(
                result='ok',
                data=self.serialize(user))
        except ValidationError as err:
            self.request.response.status_code = 422
            return dict(result='error', data=err.messages)

    @view_config(route_name='login', request_method='POST')
    def login(self):
        login = self.request.json_body['login']
        password = self.request.json_body['password']
        user = User.authenticate(login, password, self.request.dbsession)
        if user:
            return {
                'result': 'ok',
                'token': self.request.create_jwt_token(
                    user['userid'],
                    roles=user['roles'],
                    username=user['username'])
            }
        else:
            return {
                'result': 'error',
                'token': None
            }

    def logout(self):
        pass

    def reset_password(self):
        pass
