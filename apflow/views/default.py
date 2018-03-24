from pyramid.response import Response
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPNotFound

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm import load_only
from sqlalchemy.orm.exc import NoResultFound

from apflow.counterparty.models import Counterparty
from apflow.counterparty.schemas import CounterpartySchema



@view_config(route_name='counterparty', request_method='GET', renderer='json')
def counterparty_list(request):
    cp_schema = CounterpartySchema(only=('name', 'eik_egn'))
    res = request.dbsession.query
    res = res(Counterparty).filter(Counterparty.id > 20)
    return [cp_schema.dump(cp).data for cp in res]
    # q = q.options(load_only('name', 'eik_egn'))
    # return dict(data=list(q),
    #             columns=[col['name'] for col in q.column_descriptions])


@view_config(route_name='counterparty_view', request_method='GET', renderer='json')
def counterparty_view(request):
    try:
        id = request.matchdict['id']
        session = request.dbsession
        cp = session.query(Counterparty).filter_by(id=id).one()
        cp_schema = CounterpartySchema(only=('name', 'eik_egn'))
        return cp_schema.dump(cp).data
    except NoResultFound:
        raise HTTPNotFound()

    # import ipdb; ipdb.set_trace()
    # cp_schema = CounterpartySchema(only=('name', 'eik_egn'))
    # q = request.dbsession.query
    # q = q(Counterparty).filter(Counterparty.id > 20)


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
