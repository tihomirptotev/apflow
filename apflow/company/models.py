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


class CompanyUnit(BaseModel):
    """ Department, Branch or Office in the organization. """

    __tablename__ = 'company_units'

    UNIT_TYPES = [
        ('department', 'Department'),
        ('branch', 'Branch'),
        ('office', 'Office')
    ]

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(length=128), index=True, unique=True, nullable=False)
    org_type = Column(ChoiceType(UNIT_TYPES))
    parent_id = Column(Integer(), ForeignKey('company_units.id'), nullable=True)
    parent = relationship('CompanyUnit',
                            backref=backref('children'),
                            remote_side=[id])
