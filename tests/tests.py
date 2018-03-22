import unittest
import transaction
import pytest
from pyramid import testing
from sqlalchemy.exc import IntegrityError
from apflow.models import (
    get_engine,
    get_session_factory,
    get_tm_session,
)
from apflow.models.meta import Base
import apflow.models


@pytest.fixture(scope='session')
def config():
    config = testing.setUp(settings={
        'sqlalchemy.url': 'sqlite:///:memory:'
    })
    config.include('apflow.models')
    yield config
    testing.tearDown()


@pytest.fixture(scope='session')
def engine(config):
    settings = config.get_settings()
    engine = get_engine(settings)
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='function')
def dbsession(engine):
    session_factory = get_session_factory(engine)
    session = get_tm_session(session_factory, transaction.manager)
    yield session
    session.rollback()


import factory
from apflow.models import Counterparty


@pytest.fixture(scope='function')
def counterparty_factory(dbsession):
    from apflow.models import Counterparty

    class CounterPartyFactory(factory.alchemy.SQLAlchemyModelFactory):
        class Meta:
            model = Counterparty
            sqlalchemy_session = dbsession   # the SQLAlchemy session object
        id = factory.Sequence(lambda n: n)
        name = factory.Faker('company', locale='bg_BG')
        created_by = 1
        updated_by = 1

    return CounterPartyFactory


def test_create_counterparty(dbsession, counterparty_factory):
    c2 = counterparty_factory.build(eik_egn='123456789')
    with transaction.manager:
        dbsession.add(c2)
        c = dbsession.query(Counterparty).one()
        assert c.eik_egn == c2.eik_egn


def test_invalid_conterparty(dbsession, counterparty_factory):
    with pytest.raises(AssertionError):
        c = counterparty_factory.build(eik_egn='12345678901234')
    with pytest.raises(AssertionError):
        c1 = counterparty_factory.build(eik_egn='1234')



