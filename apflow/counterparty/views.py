from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy.orm.exc import NoResultFound
from .schemas import CounterpartySchema
from .models import Counterparty


class CounterpartyService:

    def __init__(self, request):
        self.request = request
        self.schema = CounterpartySchema(only=('id', 'name', 'eik_egn'))

    def list_all(self):
        session = self.request.dbsession
        return session.query(Counterparty)

    def get_by_id(self, id):
        session = self.request.dbsession
        return session.query(Counterparty).filter_by(id=id).one()

    def url_for_id(self, id):
        return self.request.route_url('counterparty_view', id=id)

    def serialize_single(self, obj):
        res = self.schema.dump(obj).data
        res['url'] = self.url_for_id(obj.id)
        return res

    def serialize_multiple(self, obj_list):
        return [self.serialize_single(obj) for obj in obj_list]


@view_defaults(renderer='json')
class CounterpartyView:
    def __init__(self, request):
        self.request = request
        self.service = CounterpartyService(request)

    @view_config(route_name='counterparty', request_method='GET')
    def counterparty_list(self):
        counterparties = self.service.list_all()
        return self.service.serialize_multiple(counterparties)

    @view_config(route_name='counterparty_view', request_method='GET')
    def counterparty_view(self):
        try:
            id = self.request.matchdict['id']
            cp = self.service.get_by_id(id)
            return self.service.serialize_single(cp)
        except NoResultFound:
            raise HTTPNotFound()

