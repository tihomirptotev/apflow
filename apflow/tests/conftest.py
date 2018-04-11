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
    User,
    Role,
)
from apflow.models.meta import Base
import apflow.models


@pytest.fixture(scope='session')
def config():
    test_settings = {
        'sqlalchemy.url': 'postgresql://apflow:devpassword@localhost:5432/apflow_testing',
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


@pytest.fixture(autouse=True)
def engine(config):
    settings = config.get_settings()
    engine = get_engine(settings)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='session')
def app(config):
    from apflow import main
    settings = config.get_settings()
    appl = main({}, **settings)
    return webapp(appl)


# @pytest.fixture(scope='session')
# def dbtables(engine):
#     Base.metadata.create_all(engine)
#     yield
#     Base.metadata.drop_all(engine)



@pytest.fixture()
def dbsession(engine):
    session_factory = get_session_factory(engine)
    session = get_tm_session(session_factory, transaction.manager)
    yield session
    session.rollback()


@pytest.fixture()
def webrequest(dbsession):
    request = testing.DummyRequest()
    request.dbsession = dbsession
    return request


@pytest.fixture(autouse=True)
def admin_user(dbsession):
    with transaction.manager:
        user = User(username='admin', email='admin@local.host',
                    password='password')
        role = Role(name='admins', description='admins description')
        user.roles.append(role)
        dbsession.add(user)
        dbsession.flush()
    return user


@pytest.fixture(autouse=True)
def sample_data(dbsession):
    import openpyxl
    from apflow.models import (
        Role, User, CompanyUnit, Employee, Counterparty, ApDocument,
        CostAccount, ApDocCostDistribution)
    wb = openpyxl.load_workbook('apflow/tests/data/test_data.xlsx')
    for model_name in (Role, User, CompanyUnit, Employee, Counterparty):
        sheetname = model_name.__tablename__
        ws = wb[sheetname]
        data = [tuple(cell.value for cell in row) for row in ws.rows]
        columns = data[0]
        data_as_dict = [dict(zip(columns, row)) for row in data[1:]]
        for item in data_as_dict:
            obj = model_name(**item)
            if model_name == User:
                obj.password = 'password'
            dbsession.add(obj)
        dbsession.flush()

    ws = wb['roles_users']
    data = [tuple(cell.value for cell in row) for row in ws.rows][1:]
    for row in data:
        user = User.get_by_id(dbsession, row[0])
        role = Role.get_by_id(dbsession, row[1])
        user.roles.append(role)
        # import ipdb; ipdb.set_trace()
        dbsession.add(user)
    dbsession.flush()
    yield
