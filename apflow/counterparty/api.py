from pyramid.view import view_defaults
from apflow.views.base_api import BaseApi
from .models import Counterparty
from .schemas import CounterpartySchema
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
        self.schema = CounterpartySchema()
        self.schema.context = {
            'request': self.request,
            'detail_route_name': 'counterparty_view'
        }
