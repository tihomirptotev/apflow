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
from marshmallow.exceptions import ValidationError


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
        self.schema.context = {
            'request': self.request,
            'detail_route_name': getattr(self.Meta, 'detail_route_name')
        }
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
        return self.schema.dump(obj)


    def list_all(self):
        res = self.request.dbsession.query(self.model)
        return dict(
            result='ok',
            data=[self.serialize(obj) for obj in res])

    def add(self):
        # import ipdb; ipdb.set_trace()
        try :
            data = self.schema.load(self.request.json_body)
            obj = self.model(**data)
            obj.created_by = self.request.authenticated_userid
            obj.updated_by = self.request.authenticated_userid
            obj.save(self.request.dbsession)
            self.request.response.status_code = 201
            return dict(
                result='ok',
                data=self.serialize(obj))
        # except IntegrityError:
        #     self.request.response.status_code = 422
        #     return dict(result='error', data='Wrong input!')
        except ValidationError as err:
            self.request.response.status_code = 422
            return dict(result='error', data=err.messages)


    def view(self):
        return self.serialize(self.obj)

    def update(self):
        try:
            data = self.schema.load(self.request.json_body)
            self.obj.update(**data)
            self.obj.updated_by = self.request.authenticated_userid
            self.obj.save(self.request.dbsession)
            self.request.response.status_code = 202
            return dict(
                result='ok',
                data=self.serialize(self.obj))
        except ValidationError as err:
            self.request.response.status_code = 422
            return dict(result='error', data=err.messages)

    def delete_soft(self):
        if self.obj.deleted:
            raise HTTPNotFound
        self.obj.soft_delete(self.request.dbsession)
        self.request.response = HTTPAccepted()
        return dict(result='Record deleted.', data=dict(id=self.obj.id))
