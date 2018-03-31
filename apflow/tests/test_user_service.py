################# Functional Api Tests #####################
from passlib.apps import custom_app_context
import pytest
from pyramid import testing
from sqlalchemy.orm.exc import NoResultFound
from apflow.user.services import UserService, RoleService
from apflow.user.models import User, Role


user_data = [
    dict(username='admin', email='admin@local.host', password='admin1'),
    dict(username='user1', email='user1@local.host', password='user1'),
    dict(username='user2', email='user2@local.host', password='user2'),
]


role_data = [
    dict(name='admins', description='admins'),
    dict(name='level1', description='level1'),
    dict(name='level2', description='level2'),
]


@pytest.fixture
def users(webrequest):
    service = UserService(webrequest)
    return [service.create(**row) for row in user_data]


@pytest.fixture
def roles(webrequest):
    service = RoleService(webrequest)
    return [service.create(**row) for row in role_data]


class TestCounterpartyService:

    def test_create(self, users, roles, webrequest):
        service = UserService(webrequest)
        user = users[0]
        assert user.check_password('admin1')
        role = roles[0]
        assert role.name == 'admins'

        service.assign_role_to_user('admin', 'admins')
        service.assign_role_to_user('admin', 'level1')

        assert service.get_by_id(1).roles[0].name == 'admins'
        assert service.get_by_id(1).roles[1].name == 'level1'
        with pytest.raises(IndexError):
            service.get_by_id(1).roles[2]

    def test_authenticate(self, admin_user, webrequest):
        service = UserService(webrequest)
        assert service.authenticate(admin_user.email, 'password')


        # obj2 = service.create(**counterparty_data[0])
        # assert obj2['result'] == 'error'
        # with pytest.raises(AssertionError):
        #     service.create(**bad_data[0])
        # with pytest.raises(AssertionError):
        #     service.create(**bad_data[1])
