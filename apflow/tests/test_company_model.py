import datetime
import pytest
from apflow.company.models import CompanyUnit, ApDocument
from apflow.counterparty.models import Counterparty


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


class TestApDocument:

    @pytest.fixture
    def counterparties_data(self, dbsession):
        counterparty_data = [
            dict(name='Company 1', eik_egn='111222333'),
            dict(name='Company 2', eik_egn='223456712'),
            dict(name='Company 3', eik_egn='323456712'),
            dict(name='ЕООД 1234', eik_egn='444444712'),
        ]
        for row in counterparty_data:
            obj = Counterparty(**row)
            obj.created_by = 1
            obj.updated_by = 1
            dbsession.add(obj)
            dbsession.flush()

    def test_create_ap_doc(self, dbsession, counterparties_data):
        data = dict(
            doc_number='001',
            counterparty_id=3,
            doc_date=datetime.date(2018, 4, 11),
            doc_sum=15.36,
            level='level_bn',
            doc_info='Info 1',
            doc_info_additional='Info 2',
            status='draft',
            created_by=1,
            updated_by=1
        )
        doc = ApDocument(**data)
        dbsession.add(doc)
        dbsession.flush()

        doc = dbsession.query(ApDocument).first()
        assert doc.doc_sum == 15.36
        assert doc.doc_date == datetime.date(2018, 4, 11)
        assert doc.counterparty.name == 'Company 3'
