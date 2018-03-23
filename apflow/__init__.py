from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.include('pyramid_jinja2')
    config.include('pyramid_jwt')
    config.set_jwt_authentication_policy('secret')
    config.include('.models')
    config.include('.routes')
    config.scan()
    return config.make_wsgi_app()
