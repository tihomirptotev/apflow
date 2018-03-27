################# Functional Api Tests #####################
import pytest
from pyramid import testing
from sqlalchemy.orm.exc import NoResultFound
from apflow.counterparty.services import CounterpartyService
from apflow.counterparty.models import Counterparty


@pytest.fixture
def service(webrequest):
    return CounterpartyService(webrequest)


counterparty_data = [
    dict(name='Company 1', eik_egn='111222333'),
    dict(name='Company 2', eik_egn='223456712'),
    dict(name='Company 3', eik_egn='323456712'),
    dict(name='ЕООД 1234', eik_egn='444444712'),
]
bad_data = [
    dict(name='Company less than 8', eik_egn='11122233'),
    dict(name='Company more than 13', eik_egn='12345678901234'),
]



class TestCounterpartyService:

    def test_create(self, service):
        obj = service.create(**counterparty_data[0])
        assert isinstance(obj, Counterparty)
        obj2 = service.create(**counterparty_data[0])
        assert obj2['result'] == 'error'
        with pytest.raises(AssertionError):
            service.create(**bad_data[0])
        with pytest.raises(AssertionError):
            service.create(**bad_data[1])
        # assert isinstance(obj2, Counterparty)

        # res = app.post_json('/counterparty/', dict(name='Company 2', eik_egn='123456719'))
        # assert res == 'ok'

    def test_create_many(self, service):
        service.create_many(counterparty_data)
        assert service.list_all().count() == 4

    def test_get_by_id(self, service):
        for d in counterparty_data:
            service.create(**d)
        obj = service.get_by_id(1)
        assert isinstance(obj, Counterparty)

    def test_find_by_col_name(self, service):
        service.create_many(counterparty_data)
        obj1 = service.find_by_col_name('eik_egn', '111222333').first()
        assert isinstance(obj1, Counterparty)
        obj = service.find_by_col_name('name', 'ЕООД 1234').first()
        assert isinstance(obj, Counterparty)

    def test_update(self, service):
        service.create_many(counterparty_data)
        service.update(1, dict(name='Updated name', eik_egn='999888777'))
        obj = service.find_by_col_name('name', 'Updated name').first()
        assert obj.id == 1

    def test_delete(self, service):
        service.create_many(counterparty_data)
        res = service.delete(1)
        assert 'id' in res.keys()
        assert service.delete(1001)['result'] == 'error'


