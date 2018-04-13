from pyramid.security import ALL_PERMISSIONS, Allow, Deny, Everyone, DENY_ALL, Authenticated
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

    def __acl__(self=None):
        # if self and (self.id == 2):
        #     return [(Allow, Everyone, ALL_PERMISSIONS)]
        # else:
        #     return [(Allow, 'admins', ALL_PERMISSIONS)]
        return [(Allow, 'admins', ALL_PERMISSIONS)]

    counterparty_id = Column(Integer(), ForeignKey('counterparties.id'))
    init_unit_id = Column(Integer(), ForeignKey('company_units.id'))
    doc_number = Column(String(length=20))
    doc_date = Column(Date, nullable=False)
    doc_sum = Column(Float)
    doc_info = Column(UnicodeText, nullable=False)
    doc_info_additional = Column(UnicodeText, nullable=True)
    doc_type = Column(String(length=30))
    level = Column(String(length=30))
    status = Column(String(length=30))
    cd_entries = relationship('ApDocCostDistribution',
                              backref='apdoc',
                              lazy='dynamic')


class ApDocCostDistribution(BaseModel):
    """ Account payable document cost distribution """

    __tablename__ = 'ap_document_cd'

    apdoc_id = Column(Integer(), ForeignKey('ap_documents.id'))
    cost_account_id = Column(Integer(), ForeignKey('cost_accounts.id'))
    company_unit_id = Column(Integer(), ForeignKey('company_units.id'))
    amount = Column(Numeric)
