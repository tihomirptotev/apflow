from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import load_only
from sqlalchemy.orm.exc import NoResultFound


@view_config(route_name='login', request_method='POST', renderer='json')
def login(request):
    login = request.POST['login']
    password = request.POST['password']
    user_id =  (login == 'user') and (password == 'password')
    # user_id = authenticate(login, password)  # You will need to implement this

    if user_id:
        return {
            'result': 'ok',
            'apflow-token': request.create_jwt_token(user_id),
            'username': 'k13totev'
        }
    else:
        return {
            'result': 'error'
        }
