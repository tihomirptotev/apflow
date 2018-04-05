import pytest
from apflow.company.models import CompanyUnit


data = [
    dict(name='Branch network', org_type='department'),
    dict(name='Stara Zagora', org_type='branch', parent_id=1),
    dict(name='Radnevo', org_type='office', parent_id=2),
    dict(name='Verea', org_type='office', parent_id=2),
    dict(name='Plovdiv', org_type='branch', parent_id=1),
    dict(name='Asenovgrad', org_type='office', parent_id=5),
]


class TestCompanyModel:

    def test_create(self, dbsession):
        for row in data:
            unit = CompanyUnit(**row)
            unit.created_by = 1
            unit.updated_by = 1
            dbsession.add(unit)
        dbsession.flush()

        res = dbsession.query(CompanyUnit).all()
        assert len(res) == 6

        branch = dbsession.query(CompanyUnit).get(2)
        assert branch.name == 'Stara Zagora'
        assert branch.children[0].name == 'Radnevo'

        dep = dbsession.query(CompanyUnit).get(1)
        assert dep.parent_id is None
        assert dep.children[1].name == 'Plovdiv'

        office = dbsession.query(CompanyUnit).get(3)
        assert office.children == []
