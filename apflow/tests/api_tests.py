################# Functional Api Tests #####################
import pytest
from pyramid import testing
from webtest.app import AppError
from apflow.counterparty.services import CounterpartyService
from apflow.counterparty.models import Counterparty

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


@pytest.mark.usefixtures('engine')
def test_counterparty_add(app, webrequest):
    # service = CounterpartyService(webrequest)
    res = app.post_json('/counterparty/', counterparty_data[0])
    assert res.status_code == 200


@pytest.mark.usefixtures('engine')
def test_counterparty_update(app, webrequest):
    # service = CounterpartyService(webrequest)
    data = {
        "name": "Updated name",
        "eik_egn": "987456124"
    }
    res = app.put_json('/counterparty/1', data)
    res1 = app.get('/counterparty/1')
    assert res1.status_code == 200
    assert res1.json['name'] == data['name']


@pytest.mark.usefixtures('engine')
def test_counterparty_delete(app, webrequest):
    res = app.post_json('/counterparty/', counterparty_data[0])
    res = app.delete_json('/counterparty/1')
    assert res.status_code == 200

    with pytest.raises(AppError):
        res = app.delete_json('/counterparty/100')
    # assert res1.json['name'] == data['name']
