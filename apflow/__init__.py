import json
from pyramid.config import Configurator
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import notfound_view_config
from pyramid.response import Response
from pyramid.security import ALL_PERMISSIONS, Allow, Deny, Everyone, DENY_ALL, Authenticated


class RootACL(object):
    __acl__ = [
        (Allow, 'admins', ALL_PERMISSIONS)
    ]

    def __init__(self, request):
        pass


@notfound_view_config(request_method=['GET', 'PUT', 'DELETE'], renderer='json')
def notfound(request):
    request.response = HTTPNotFound()
    return dict(
        result='error',
        data='Requested resource not found.'
    )


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
