from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    Unicode,
    UnicodeText,
    ForeignKey, String
)
from sqlalchemy.orm import relationship, backref
from apflow.models.meta import Base
from apflow.models.mixins import SurrogatePK, AuditMixin


class Counterparty(AuditMixin, Base):
    # __versioned__ = {}
    __tablename__ = 'counterparties'
    # id = Column(Integer, primary_key=True)
    name = Column(Unicode(length=50), index=True)
    eik_egn = Column(String(13), index=True, unique=True)


class CounterpartyNote(AuditMixin, Base):
    __tablename__ = 'counterparty_notes'
    # id = Column(Integer, primary_key=True)
    note = Column(UnicodeText(500), index=True)
    counterparty_id = Column(Integer(), ForeignKey('counterparties.id'))
    counterparty = relationship('Counterparty',
                                backref=backref('notes'))
