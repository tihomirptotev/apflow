import pytest
from apflow.company.models import CompanyUnit, Employee
from apflow.user.models import User, Role


units_data = [
    dict(name='Branch network', org_type='department'),
    dict(name='Stara Zagora', org_type='branch', parent_id=1),
    dict(name='Radnevo', org_type='office', parent_id=2),
    dict(name='Verea', org_type='office', parent_id=2),
    dict(name='Plovdiv', org_type='branch', parent_id=1),
    dict(name='Asenovgrad', org_type='office', parent_id=5),
]

user_data = [
    dict(username='brnetman', email='brnetman@local.host', password='password'),
    dict(username='brman1', email='brman1@local.host', password='password'),
    dict(username='bremp1', email='bremp1@local.host', password='password'),
]

roles_data = [
    dict(name='bnet_manager', description='Branch network manager info'),
    dict(name='b_manager', description='Branch manager info'),
    dict(name='b_accountant', description='Branch accountant info'),
]

employees_data = [
    dict(name='Name bnet manager', company_unit_id=1, user_id=1),
    dict(name='Name br manager', company_unit_id=2, user_id=2),
    dict(name='Name br acc', company_unit_id=2, user_id=3),
]


class TestCompanyUserRelationship:

    def test_create(self, dbsession):
        roles = []
        for row in roles_data:
            role = Role(**row)
            role.created_by = 1
            role.updated_by = 1
            dbsession.add(role)
            roles.append(role)

        for i, row in enumerate(user_data):
            user = User(**row)
            user.created_by = 1
            user.updated_by = 1
            user.roles.append(roles[i])
            dbsession.add(user)

        for row in units_data:
            unit = CompanyUnit(**row)
            unit.created_by = 1
            unit.updated_by = 1
            dbsession.add(unit)

        dbsession.flush()

        for row in employees_data:
            emp = Employee(**row)
            emp.created_by = 1
            emp.updated_by = 1
            dbsession.add(emp)

        dbsession.flush()

        res = dbsession.query(CompanyUnit).all()
        assert len(res) == 6

        branch = dbsession.query(CompanyUnit).get(2)
        assert branch.name == 'Stara Zagora'
        assert branch.children[0].name == 'Radnevo'
        assert branch.staff[0].name == 'Name br manager'
        assert branch.staff[0].user.username == 'brman1'

        dep = dbsession.query(CompanyUnit).get(1)
        assert dep.parent_id is None
        assert dep.children[1].name == 'Plovdiv'

        office = dbsession.query(CompanyUnit).get(3)
        assert office.children == []


        query = dbsession.query(
            CompanyUnit.name, Employee.name, User.username, Role.name)
        query = query.join(Employee).join(User).join(User.roles).filter(
            CompanyUnit.id == 1)
        res = query.all()
        assert len(res) == 2
