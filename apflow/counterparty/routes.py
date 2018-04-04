def includeme(config):
    config.add_route('counterparty', '/')
    config.add_route('counterparty_view', '/{id}')
    config.add_view('apflow.counterparty.api.CounterpartyApi',
                    route_name='counterparty',
                    request_method='GET',
                    permission='read',
                    attr='list_all')
    config.add_view('apflow.counterparty.api.CounterpartyApi',
                    route_name='counterparty',
                    request_method='POST',
                    permission='crud',
                    attr='add')
    config.add_view('apflow.counterparty.api.CounterpartyApi',
                    route_name='counterparty_view',
                    request_method='GET',
                    permission='read',
                    attr='view')
    config.add_view('apflow.counterparty.api.CounterpartyApi',
                    route_name='counterparty_view',
                    request_method='PUT',
                    permission='crud',
                    attr='update')
    config.add_view('apflow.counterparty.api.CounterpartyApi',
                    route_name='counterparty_view',
                    request_method='DELETE',
                    permission='crud',
                    attr='delete')

# TODO: Add permissions
