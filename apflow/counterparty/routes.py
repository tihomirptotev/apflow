def includeme(config):
    config.add_route('counterparty', '/')
    config.add_route('counterparty_view', '/{id}')
