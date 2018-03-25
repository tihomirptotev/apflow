from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPNotFound
from sqlalchemy.orm.exc import NoResultFound
from .services import CounterpartyService


@view_defaults(renderer='json')
class CounterpartyView:
    def __init__(self, request):
        self.request = request
        self.service = CounterpartyService(request)
        self.user_id = 1

    @view_config(route_name='counterparty', request_method='GET')
    def counterparty_list(self):
        counterparties = self.service.list_all()
        return self.service.serialize_multiple(counterparties)

    @view_config(route_name='counterparty', request_method='POST', renderer='json')
    def counterparty_add(self):
        cp = self.service.create(json_data=self.request.json_body)
        return self.service.serialize_single(cp)

    @view_config(route_name='counterparty_view', request_method='GET')
    def counterparty_view(self):
        try:
            id = self.request.matchdict['id']
            cp = self.service.get_by_id(id)
            return self.service.serialize_single(cp)
        except NoResultFound:
            raise HTTPNotFound()

