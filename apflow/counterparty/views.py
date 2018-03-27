import json
from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden, HTTPClientError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from .services import CounterpartyService
from .models import Counterparty


@view_defaults(renderer='json')
class CounterpartyView:
    def __init__(self, request):
        self.request = request
        self.service = CounterpartyService(request)
        self.user_id = 1
        if self.request.matchdict:
            self.id = self.request.matchdict['id']
            try:
                self.obj = self.service.get_by_id(self.id)
            except NoResultFound:
                raise HTTPNotFound


    @view_config(route_name='counterparty', request_method='GET')
    def counterparty_list(self):
        counterparties = self.service.list_all()
        return self.service.serialize_multiple(counterparties)

    @view_config(route_name='counterparty', request_method='POST', renderer='json')
    def counterparty_add(self):
        # import ipdb; ipdb.set_trace()
        res = self.service.deserialize_single(self.request.json_body)
        msg = ''
        if res.errors:
            msg = dict(result='error', data=res.errors, code=400)
        obj = self.service.create(**res.data)
        if isinstance(obj, Counterparty):
            return self.service.serialize_single(obj)
        else:
            self.request.response.status = '400 Bad Request'
            self.request.response.code = 400
            self.request.response.content_type = 'application/json'
            return dict(obj)


    @view_config(route_name='counterparty_view', request_method='GET')
    def counterparty_view(self):
        return self.service.serialize_single(self.obj)

    @view_config(route_name='counterparty_view', request_method='PUT')
    def counterparty_update(self):
        res = self.service.deserialize_single(self.request.json_body)
        if res.errors:
            return dict(result='error', data=res.errors, code=400)
        # import ipdb; ipdb.set_trace()
        obj = self.service.update(self.id, res.data)
        return self.service.serialize_single(obj)

    @view_config(route_name='counterparty_view', request_method='DELETE')
    def counterparty_delete(self):
        res = self.service.delete(self.id)
        if res.get('result') == 'error':
            return HTTPNotFound(detail=res)
        else:
            return dict(result='Record deleted.', data=res)


