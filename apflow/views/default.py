from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from ..models import Counterparty


@view_config(route_name='home', renderer='json')
def my_view(request):
    # try:
    #     query = request.dbsession.query(Counterparty)
    #     one = query.filter(Counterparty.name == 'Supplier 1').first()
    # except DBAPIError:
    #     return Response(db_err_msg, content_type='text/plain', status=500)
    # return {'one': request.authenticated_userid, 'project': 'Accounts Payable Workflow'}
    return{'name': request.authenticated_userid}


db_err_msg = """\
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to run the "initialize_apflow_db" script
    to initialize your database tables.  Check your virtual
    environment's "bin" directory for this script and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.

After you fix the problem, please restart the Pyramid application to
try it again.
"""


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
