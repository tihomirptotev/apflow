################# Functional Api Tests #####################
import pytest
from pyramid import testing
from sqlalchemy.orm.exc import NoResultFound
from apflow.user.models import User


@pytest.fixture
def service(webrequest):
    return UserService(webrequest)


user_data = [
    dict(username='admin', email='admin@local.host', password='1234'),
]

role_data = [
    dict(name='admin_user', description='Admin group'),
    dict(name='power_user', description='Power user group')
]




class TestUserService:

    def test_create(self, service, webrequest):
        obj = service.create(**user_data[0])
        assert isinstance(obj, User)

        role_service = RoleService(webrequest)
        role_service.create_many(role_data)
        assert len(role_service.list_all().all()) == 2

        user = service.assign_role_to_user('admin', 'admin_user')

        print(user.roles)
        assert user.roles[0].name == 'admin_user'

        with pytest.raises(PermissionError):
            assert obj.password == '1234'
        assert obj.check_password('1234')

        # obj2 = service.create(**counterparty_data[0])
        # assert obj2['result'] == 'error'
        # with pytest.raises(AssertionError):
        #     service.create(**bad_data[0])
        # with pytest.raises(AssertionError):
        #     service.create(**bad_data[1])
        # assert isinstance(obj2, Counterparty)

        # res = app.post_json('/counterparty/', dict(name='Company 2', eik_egn='123456719'))
        # assert res == 'ok'

    # def test_create_many(self, service):
    #     service.create_many(counterparty_data)
    #     assert service.list_all().count() == 4

    # def test_get_by_id(self, service):
    #     for d in counterparty_data:
    #         service.create(**d)
    #     obj = service.get_by_id(1)
    #     assert isinstance(obj, Counterparty)

    # def test_find_by_col_name(self, service):
    #     service.create_many(counterparty_data)
    #     obj1 = service.find_by_col_name('eik_egn', '111222333').first()
    #     assert isinstance(obj1, Counterparty)
    #     obj = service.find_by_col_name('name', 'ЕООД 1234').first()
    #     assert isinstance(obj, Counterparty)

    # def test_update(self, service):
    #     service.create_many(counterparty_data)
    #     service.update(1, dict(name='Updated name', eik_egn='999888777'))
    #     obj = service.find_by_col_name('name', 'Updated name').first()
    #     assert obj.id == 1

    # def test_delete(self, service):
    #     service.create_many(counterparty_data)
    #     res = service.delete(1)
    #     assert 'id' in res.keys()
    #     assert service.delete(1001)['result'] == 'error'
