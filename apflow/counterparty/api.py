from pyramid.view import view_defaults, view_config
from apflow.views.base_api import BaseApi
from marshmallow import fields, ValidationError
from .models import Counterparty
from .schemas import CounterpartyNoteSchema, counterparty_schema_factory
from pyramid.security import ALL_PERMISSIONS, Allow, Deny, Everyone, DENY_ALL, Authenticated


@view_defaults(renderer='json')
class CounterpartyApi(BaseApi):

    # __acl__ = [
    #         # (Allow, 'admins', ALL_PERMISSIONS)
    #         (Allow, Everyone, ALL_PERMISSIONS)
    #     ]

    def __init__(self, context, request):
        super().__init__(request)
        self.context = context
        self.schema_notes = CounterpartyNoteSchema(
            request=self.request, detail_route_name='counterparty_note_view')
        self.schema = counterparty_schema_factory(request)

    @view_config(route_name='counterparty_view', request_method='GET',
                 permission='read')
    def view(self):
        return self.context.serialize(self.schema)




    @view_config(route_name='counterparty_notes',
                 request_method='GET', permission='read')
    def list_notes_for_counterparty(self):
        notes = self.context.notes
        return dict(
            result='ok',
            data=[obj.serialize(self.schema_notes) for obj in notes])

    @view_config(route_name='counterparty_notes',
                 request_method='POST', permission='crud')
    def add_note_for_counterparty(self):
        try:
            note = self.schema_notes.load(
                self.request.json_body, self.request.dbsession)
            note.created_by = self.request.authenticated_userid
            note.updated_by = self.request.authenticated_userid
            note.counterparty_id = self.context.id
            self.context.notes.append(note)
            self.context.save(self.request.dbsession)
            self.request.response.status_code = 201
            return dict(
                result='ok',
                data=note.serialize(self.schema_notes))
        except ValidationError as err:
            self.request.response.status_code = 422
            return dict(result='error', data=err.messages)


@view_defaults(renderer='json')
class CounterpartyNoteApi(BaseApi):

    # __acl__ = [
    #         # (Allow, 'admins', ALL_PERMISSIONS)
    #         (Allow, Everyone, ALL_PERMISSIONS)
    #     ]

    def __init__(self, context, request):
        super().__init__(request)
        self.context = context
        self.schema = CounterpartyNoteSchema(
            request=self.request, detail_route_name='counterparty_note_view')
