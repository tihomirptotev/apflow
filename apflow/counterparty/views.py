from pyramid.view import view_defaults
from apflow.views.base_views import BaseView
from .services import CounterpartyService
from .models import Counterparty



@view_defaults(route_name='counterparty', renderer='json', permission='view')
class CounterpartyView(BaseView):
    model_class = Counterparty
    service_class = CounterpartyService
