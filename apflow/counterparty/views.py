from pyramid.view import view_defaults
from apflow.views.base_api import BaseApi
from .models import Counterparty
from .schemas import CounterpartySchema


@view_defaults(renderer='json')
class CounterpartyApi(BaseApi):

    class Meta:
        model_class = Counterparty
        schema = CounterpartySchema(only=('id', 'name', 'eik_egn'))
        detail_route_name = 'counterparty_view'
