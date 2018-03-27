import json
from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPNotFound, HTTPForbidden, HTTPClientError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from .services import CounterpartyService
from .models import Counterparty



class BaseView:
    model_class = None
    service_class = None

    def __init__(self, request):
        self.request = request
        self.service = self.service_class(request)
        self.user_id = 1
        if self.request.matchdict:
            self.id = self.request.matchdict['id']
            try:
                self.obj = self.service.get_by_id(self.id)
            except NoResultFound:
                raise HTTPNotFound

    def all(self):
        objects = self.service.list_all()
        return self.service.serialize_multiple(objects)

    def add(self):
        # import ipdb; ipdb.set_trace()
        res = self.service.deserialize_single(self.request.json_body)
        if res.errors:
            msg = dict(result='error', data=res.errors, code=400)
        obj = self.service.create(**res.data)
        if isinstance(obj, self.model_class):
            return self.service.serialize_single(obj)
        else:
            self.request.response.status = '400 Bad Request'
            self.request.response.code = 400
            self.request.response.content_type = 'application/json'
            return dict(obj)

    def view(self):
        return self.service.serialize_single(self.obj)

    def update(self):
        res = self.service.deserialize_single(self.request.json_body)
        if res.errors:
            return dict(result='error', data=res.errors, code=400)
        # import ipdb; ipdb.set_trace()
        obj = self.service.update(self.id, res.data)
        return self.service.serialize_single(obj)

    def delete(self):
        res = self.service.delete(self.id)
        if res.get('result') == 'error':
            return HTTPNotFound(detail=res)
        else:
            return dict(result='Record deleted.', data=res)



@view_defaults(route_name='counterparty', renderer='json')
class CounterpartyView(BaseView):
    model_class = Counterparty
    service_class = CounterpartyService
