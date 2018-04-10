import pytest
from apflow.company.models import CompanyUnit, Employee
from apflow.user.models import User, Role

@pytest.fixture(autouse=True)
def sample_data(dbsession):
    import openpyxl
    wb = openpyxl.load_workbook('apflow/tests/data/test_data.xlsx')
    for model_name in (Role, User, CompanyUnit, Employee):
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



class TestCompanyUserRelationship:

    def test_create(self, dbsession):
        res = dbsession.query(CompanyUnit).all()
        assert len(res) == 7

        branch = dbsession.query(CompanyUnit).get(2)
        assert branch.name == 'Branch_1'
        assert branch.children[0].name == 'Branch_1_office_1'
        assert branch.staff[0].name == 'b1_man_full_name'
        assert branch.staff[0].user.username == 'b1_man_name'

        dep = dbsession.query(CompanyUnit).get(1)
        assert dep.parent_id is None
        assert dep.children[1].name == 'Branch_2'

        office = dbsession.query(CompanyUnit).get(3)
        assert office.children == []


        query = dbsession.query(
            CompanyUnit.name, Employee.name, User.username, Role.name)
        query = query.join(Employee).join(User).join(User.roles).filter(
            CompanyUnit.id == 1)
        res = query.all()
        assert len(res) == 1
