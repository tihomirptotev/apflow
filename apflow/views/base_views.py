import json
from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import (
    HTTPNotFound,
    HTTPForbidden,
    HTTPClientError,
    HTTPCreated,
    HTTPAccepted,
)
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError


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
        # import ipdb; ipdb.set_trace()
        objects = self.service.list_all()
        return self.service.serialize_multiple(objects)

    def add(self):
        # import ipdb; ipdb.set_trace()
        res = self.service.deserialize_single(self.request.json_body)
        if res.errors:
            self.request.response.status_code = 400
            # self.request.response = HTTPClientError()
            return dict(result='error', data=res.errors)
            # return {}
        else:
            obj = self.service.create(**res.data)
            self.request.response = HTTPCreated()
            return dict(
                result='ok',
                data=self.service.serialize_single(obj))

    def view(self):
        return self.service.serialize_single(self.obj)

    def update(self):
        res = self.service.deserialize_single(self.request.json_body)
        if res.errors:
            self.request.response.status_code = 400
            return dict(result='error', data=res.errors)
        else:
            try:
                obj = self.service.update(self.id, res.data)
                self.request.response = HTTPAccepted()
                return dict(
                    result='ok',
                    data=self.service.serialize_single(obj))
            except:
                raise HTTPNotFound

    def delete(self):
        try:
            obj = self.service.delete(self.id)
            self.request.response = HTTPAccepted()
            return dict(result='Record deleted.',
                        data=self.service.serialize_single(obj))
        except:
            raise HTTPNotFound
