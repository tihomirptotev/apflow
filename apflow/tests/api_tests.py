################# Functional Api Tests #####################
import json
from subprocess import call
import pytest
from pyramid import testing
import requests
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


@pytest.fixture(scope='session')
def db():
    call('apflow development.ini db init', shell=True)
    yield
    call('apflow development.ini db drop_all', shell=True)


@pytest.mark.usefixtures('db')
@pytest.fixture
def token():
    r = requests.post('http://localhost:6543/login',
                      json.dumps(dict(login='admin', password='password')))
    token  = r.json()['token']
    return token


@pytest.mark.usefixtures('db')
def test_login():
    r = requests.post('http://localhost:6543/login',
                      json.dumps(dict(login='admin', password='password')))
    assert r.json()['result'] == 'ok'


@pytest.mark.usefixtures('db')
def test_counterparty_api(token):
    headers = {'Authorization': f'JWT {token}'}
    bad_headers = {'Authorization': f'JWT {token[1:]}'}
    # Create new object
    res = requests.post('http://localhost:6543/counterparty/',
                        json.dumps(counterparty_data[0]),
                        headers=headers)
    assert res.status_code == 201
    assert res.json()['result'] == 'ok'
    # Create new object - bad data
    res = requests.post('http://localhost:6543/counterparty/',
                        json.dumps(bad_data[0]),
                        headers=headers)
    assert res.status_code == 400
    assert res.json()['result'] == 'error'
    # Create new object with bad token
    res = requests.post('http://localhost:6543/counterparty/',
                        json.dumps(counterparty_data[1]),
                        headers=bad_headers)
    assert res.status_code == 403

    # Update object
    data = {
        "name": "Updated name",
        "eik_egn": "987456124"
    }
    res = requests.put('http://localhost:6543/counterparty/1',
                        json.dumps(data),
                        headers=headers)
    assert res.status_code == 202
    assert res.json()['result'] == 'ok'

    # Delete object
    res = requests.delete('http://localhost:6543/counterparty/1',
                          headers=headers)
    assert res.status_code == 202

    res = requests.delete('http://localhost:6543/counterparty/2',
                          headers=headers)
    assert res.status_code == 404
