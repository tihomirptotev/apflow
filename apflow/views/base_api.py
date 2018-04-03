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


class BaseApi:

    class Meta:
        model_class = None
        schema = None
        detail_route_name = None


    def __init__(self, request):
        self.request = request
        self.user_id = self.request.authenticated_userid
        self.model = getattr(self.Meta, 'model_class')
        self.schema = getattr(self.Meta, 'schema')
        self.schema.request = self.request
        self.detail_route_name = getattr(self.Meta, 'detail_route_name')
        if self.request.matchdict:
            try:
                self.id = self.request.matchdict['id']
                self.obj = self.model.get_by_id(
                    self.request.dbsession, self.id)
            except NoResultFound:
                raise HTTPNotFound

    def serialize(self, obj):
        """Serialize record with marshmallow."""
        res = self.schema.dump(obj)
        res.data['url'] = self.request.route_url(
            self.detail_route_name, id=obj.id)
        return res.data

    def list_all(self):
        res = self.request.dbsession.query(self.model)
        return dict(
            result='ok',
            data=[self.serialize(obj) for obj in res])

    def add(self):
        res = self.schema.load(self.request.json_body)
        if res.errors:
            self.request.response.status_code = 422
            return dict(result='error', data=res.errors)
        else:
            try:
                # import ipdb; ipdb.set_trace()
                obj = self.model(**res.data)
                obj.created_by = self.request.authenticated_userid
                obj.updated_by = self.request.authenticated_userid
                self.request.dbsession.add(obj)
                self.request.dbsession.flush()
                self.request.response = HTTPCreated()
                return dict(
                    result='ok',
                    data=self.serialize(obj))
            except IntegrityError:
                self.request.response.status_code = 422
                return dict(result='error', data='Wrong input!')


    def view(self):
        return self.serialize(self.obj)

    def update(self):
        res = self.schema.load(self.request.json_body)
        if res.errors:
            self.request.response.status_code = 422
            return dict(result='error', data=res.errors)
        else:
            for k, v in res.data.items():
                setattr(self.obj, k, v)
            self.obj.updated_by = self.request.authenticated_userid
            self.request.dbsession.add(self.obj)
            self.request.dbsession.flush()
            self.request.response = HTTPAccepted()
            return dict(
                result='ok',
                data=self.serialize(self.obj))

    def delete(self):
        self.request.dbsession.delete(self.obj)
        self.request.response = HTTPAccepted()
        return dict(result='Record deleted.', data=self.obj.id)
