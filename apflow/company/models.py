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
)
from sqlalchemy.orm import relationship, backref, validates
from sqlalchemy_utils.types.choice import ChoiceType
from apflow.models.mixins import BaseModel

UNIT_TYPES = [
    ('department', 'Department'),
    ('branch', 'Branch'),
    ('office', 'Office')
]


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
    # info = Column(Unicode(length=512))
