from pyramid.response import Response
from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPNotFound

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import load_only
from sqlalchemy.orm.exc import NoResultFound
from apflow.user.services import UserService


@view_defaults(renderer='json')
class AuthView:

    def __init__(self, request):
        self.request = request
        self.service = UserService(self.request)

    def register(self):
        # Need to check if username or email exists
        pass

    @view_config(route_name='login', request_method='POST')
    def login(self):
        login = self.request.json_body['login']
        password = self.request.json_body['password']
        user = self.service.authenticate(login, password)
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
