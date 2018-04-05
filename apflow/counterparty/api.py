from pyramid.view import view_defaults
from apflow.views.base_api import BaseApi
from .models import Counterparty
from .schemas import CounterpartySchema
from pyramid.security import ALL_PERMISSIONS, Allow, Deny, Everyone, DENY_ALL, Authenticated


@view_defaults(renderer='json')
class CounterpartyApi(BaseApi):

    __acl__ = [
            (Allow, 'admins', 'crud')
        ]

    class Meta:
        model_class = Counterparty
        # schema = CounterpartySchema(only=('id', 'name', 'eik_egn'))
        schema = CounterpartySchema()
        detail_route_name = 'counterparty_view'
