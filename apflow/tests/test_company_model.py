import datetime
import pytest
from apflow.company.models import CompanyUnit
from apflow.apdoc.models import ApDocument
from apflow.counterparty.models import Counterparty



class TestCompanyModel:

    def test_company(self, dbsession):
        res = dbsession.query(CompanyUnit).all()
        assert len(res) == 7

        branch = dbsession.query(CompanyUnit).get(2)
        assert branch.name == 'Branch_1'
        assert branch.children[0].name == 'Branch_1_office_1'


class TestApDocument:

    def test_create_ap_doc(self, dbsession):
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
