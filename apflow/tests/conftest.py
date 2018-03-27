import unittest
import transaction
import pytest
from pyramid import testing
from webtest import TestApp as webapp
from pyramid.authorization import ACLAuthorizationPolicy
from sqlalchemy.exc import IntegrityError
from apflow import add_role_principals
from apflow.models import (
    get_engine,
    get_session_factory,
    get_tm_session,
)
from apflow.models.meta import Base
import apflow.models


@pytest.fixture(scope='session')
def config():
    test_settings = {
        'sqlalchemy.url': 'sqlite:///apflow_testdb.sqlite',
        'auth.secret': 'sekret',
    }
    config = testing.setUp(settings=test_settings)
    config.set_authorization_policy(ACLAuthorizationPolicy())
    config.include('pyramid_jwt')
    config.set_jwt_authentication_policy(
        test_settings['auth.secret'],
        auth_type='Bearer',
        callback=add_role_principals)
    config.include('..models')
    config.include('..routes')
    config.scan()
    yield config
    testing.tearDown()


@pytest.fixture(scope='session')
def app(config):
    from apflow import main
    settings = config.get_settings()
    appl = main({}, **settings)
    return webapp(appl)


@pytest.fixture(scope='module')
def engine(config):
    settings = config.get_settings()
    engine = get_engine(settings)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

# @pytest.fixture(scope='session')
# def dbtables(engine):
#     Base.metadata.create_all(engine)
#     yield
#     Base.metadata.drop_all(engine)



@pytest.fixture(scope='function')
def dbsession(engine):
    session_factory = get_session_factory(engine)
    session = get_tm_session(session_factory, transaction.manager)
    yield session
    session.rollback()


@pytest.fixture(scope='function')
def webrequest(dbsession):
    request = testing.DummyRequest()
    request.dbsession = dbsession
    return request
