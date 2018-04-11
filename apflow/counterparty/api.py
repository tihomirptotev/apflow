from pyramid.view import view_defaults
from apflow.views.base_api import BaseApi
from marshmallow import fields
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
