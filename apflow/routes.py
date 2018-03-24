def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('counterparty', '/counterparty')
    config.add_route('counterparty_view', '/counterparty/{id}')
    config.add_route('login', '/login')
