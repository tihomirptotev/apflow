from pyramid.view import view_config


def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.include('apflow.counterparty.routes', route_prefix='/counterparty')
    config.add_route('login', '/login')
