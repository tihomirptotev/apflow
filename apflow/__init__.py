import json
from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.view import notfound_view_config
from pyramid.response import Response
from pyramid.security import ALL_PERMISSIONS, Allow, Deny, Everyone, DENY_ALL, Authenticated


class RootACL(object):
    __acl__ = [
        (Allow, 'admin', ALL_PERMISSIONS)
    ]

    def __init__(self, request):
        pass


@notfound_view_config(request_method='GET', renderer='json')
def notfound(request):
    msg = 'Resource not found.'
    request.response.status = '404 - Not Found'
    request.response.code = 404
    request.response.content_type = 'application/json'
    return dict(
        message=msg,
        status='404 Not Found',
        code=404)


def add_role_principals(userid, request):
    # import ipdb; ipdb.set_trace()
    return request.jwt_claims.get('roles', [])


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.set_root_factory(RootACL)
    # config.include('pyramid_jinja2')
    config.include('pyramid_jwt')
    config.set_jwt_authentication_policy(
        settings['auth.secret'],
        callback=add_role_principals)
    config.include('.models')
    config.include('.routes')
    config.scan()
    return config.make_wsgi_app()
