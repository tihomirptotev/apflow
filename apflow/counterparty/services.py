from .schemas import CounterpartySchema
from .models import Counterparty
from apflow.services.base_services import ModelService


class CounterpartyService(ModelService):
    class Meta:
        model = Counterparty
        schema = CounterpartySchema(only=('id', 'name', 'eik_egn'))
        route_view_name = 'counterparty_view'
