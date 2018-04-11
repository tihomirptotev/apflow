from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Unicode,
    UnicodeText,
    ForeignKey,
    String,
    Boolean,
    Date,
    Float,
    Numeric
)
from sqlalchemy.orm import relationship, backref, validates
from sqlalchemy_utils.types.choice import ChoiceType
from apflow.models.mixins import BaseModel
from apflow.models.data import (
    UNIT_TYPES,
    AP_DOCUMENT_APPROVAL_LEVELS,
    AP_DOCUMENT_TYPES,
    AP_WORKFLOW_STATUS_CODES
)

class CompanyUnit(BaseModel):
    """ Department, Branch or Office in the organization. """

    __tablename__ = 'company_units'

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(length=128), index=True, unique=True, nullable=False)
    org_type = Column(ChoiceType(UNIT_TYPES))
    parent_id = Column(Integer(), ForeignKey('company_units.id'), nullable=True)
    parent = relationship('CompanyUnit',
                            backref=backref('children'),
                            remote_side=[id])
    staff = relationship('Employee',
                         backref=backref('company_unit'),
                         lazy='dynamic')


class Employee(BaseModel):
    """ Staff model """

    __tablename__ = 'employees'

    name = Column(Unicode(length=128), index=True, nullable=False)
    company_unit_id = Column(Integer(), ForeignKey('company_units.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', uselist=False, back_populates='employee')
    active = Column(Boolean(name='active_bool'), default=True, nullable=False)
    info = Column(Unicode(length=512))


class CostAccount(BaseModel):
    """ Accounts used for cost accounting """

    __tablename__ = 'cost_accounts'

    acc_number = Column(String(length=10), index=True,
                        unique=True, nullable=False)
    name = Column(Unicode(length=128), index=True, nullable=False)
    active = Column(Boolean(name='active_bool'), default=True, nullable=False)


class ApDocument(BaseModel):
    """ Account payable document """

    __tablename__ = 'ap_documents'

    counterparty_id = Column(Integer(), ForeignKey('counterparties.id'))
    doc_number = Column(String(length=20))
    doc_date = Column(Date, nullable=False)
    doc_sum = Column(Numeric)
    doc_info = Column(UnicodeText, nullable=False)
    doc_info_additional = Column(UnicodeText, nullable=True)
    doc_type = Column(ChoiceType(AP_DOCUMENT_TYPES))
    level = Column(ChoiceType(AP_DOCUMENT_APPROVAL_LEVELS))
    status = Column(ChoiceType(AP_WORKFLOW_STATUS_CODES))


class ApDocCostDistribution(BaseModel):
    """ Account payable document cost distribution """

    __tablename__ = 'ap_document_cd'

    apdoc_id = Column(Integer(), ForeignKey('ap_documents.id'))
    cost_account_id = Column(Integer(), ForeignKey('cost_accounts.id'))
    company_unit_id = Column(Integer(), ForeignKey('company_units.id'))
    amount = Column(Numeric)
