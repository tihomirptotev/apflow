from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import load_only
from sqlalchemy.orm.exc import NoResultFound
from apflow.user.services import UserService


@view_config(route_name='login', request_method='POST', renderer='json')
def login(request):
    # import ipdb; ipdb.set_trace()
    login = request.json_body['login']
    password = request.json_body['password']
    service = UserService(request)
    user = service.authenticate(login, password)
    # user_id = authenticate(login, password)  # You will need to implement this

    if user:
        return {
            'result': 'ok',
            'token': request.create_jwt_token(
                user['userid'],
                roles=user['roles'],
                username=user['username'])
        }
    else:
        return {
            'result': 'error',
            'token': None
        }
