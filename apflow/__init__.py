from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.view import notfound_view_config
from pyramid.response import Response
import json


@notfound_view_config(request_method='GET', renderer='json')
def notfound(request):
    return dict(
        message='Resource not found.',
        status='404 Not Found',
        code=404,
        content_type='application/json')


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
