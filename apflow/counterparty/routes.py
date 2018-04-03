def includeme(config):
    config.add_route('counterparty', '/')
    config.add_route('counterparty_view', '/{id}')
    config.add_view('apflow.counterparty.views.CounterpartyApi', route_name='counterparty', attr='list_all')
    config.add_view('apflow.counterparty.views.CounterpartyApi',
                    route_name='counterparty', request_method='POST', attr='add')
    config.add_view('apflow.counterparty.views.CounterpartyApi',
                    route_name='counterparty_view', attr='view')
    config.add_view('apflow.counterparty.views.CounterpartyApi',
                    route_name='counterparty_view', request_method='PUT', attr='update')
    config.add_view('apflow.counterparty.views.CounterpartyApi',
                    route_name='counterparty_view', request_method='DELETE', attr='delete')
