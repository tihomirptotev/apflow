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

    def __init__(self, request):
        self.request = request
        self.user_id = self.request.authenticated_userid
        self.context = None
        self.schema = None

    def list_all(self):
        res = self.request.dbsession.query(self.context)
        return dict(
            result='ok',
            data=[obj.serialize(self.schema) for obj in res])

    def add(self):
        # import ipdb; ipdb.set_trace()
        try :
            obj = self.schema.load(
                self.request.json_body, self.request.dbsession)
            obj.created_by = self.request.authenticated_userid
            obj.updated_by = self.request.authenticated_userid
            obj.save(self.request.dbsession)
            self.request.response.status_code = 201
            return dict(
                result='ok',
                data=obj.serialize(self.schema))
        # except IntegrityError:
        #     self.request.response.status_code = 422
        #     return dict(result='error', data='Wrong input!')
        except ValidationError as err:
            self.request.response.status_code = 422
            return dict(result='error', data=err.messages)


    def view(self):
        return self.context.serialize(self.schema)

    def update(self):
        try:
            obj = self.schema.load(self.request.json_body,
                                    self.request.dbsession,
                                    instance=self.context)
            # self.context.update(**data)
            obj.updated_by = self.request.authenticated_userid
            obj.save(self.request.dbsession)
            self.request.response.status_code = 202
            return dict(
                result='ok',
                data=self.context.serialize(self.schema))
        except ValidationError as err:
            self.request.response.status_code = 422
            return dict(result='error', data=err.messages)

    def delete(self):
        self.context.delete(self.request.dbsession)
        self.request.response = HTTPAccepted()
        return dict(result='Record deleted.', data=dict(id=self.context.id))


def model_factory(request, model):
    """ Creates route factory for the provided model. """
    obj_id = request.matchdict.get('id')
    if obj_id is None:
        # Return the class
        return model
    obj = request.dbsession.query(model).filter_by(id=int(obj_id)).first()
    if not obj:
        raise HTTPNotFound()
    return obj
