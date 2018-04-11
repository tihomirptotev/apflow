import pytest
from apflow.company.models import CompanyUnit, Employee
from apflow.user.models import User, Role
from apflow.counterparty.models import Counterparty, CounterpartyNote
# from apflow.counterparty.schemas import CounterpartySchema, CounterpartyNoteSchema


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


class TestCounterparty:

    def test_serialize(self, dbsession, app, webrequest):
        res = dbsession.query(CounterpartyNote).first()
        assert res.note == 'Note 2'
