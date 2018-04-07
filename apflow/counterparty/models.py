import functools
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
from sqlalchemy.schema import CheckConstraint
from apflow.views.base_api import model_factory
from apflow.models.mixins import BaseModel


class Counterparty(BaseModel):
    # __versioned__ = {}
    __tablename__ = 'counterparties'

    name = Column(Unicode(length=50), index=True, nullable=False)
    eik_egn = Column(Unicode(13), index=True, unique=True, nullable=False)
    notes = relationship('CounterpartyNote',
                         backref=backref('counterparty'),
                         lazy='dynamic')
    accounts = relationship('CounterpartyAccount',
                            backref=backref('counterparty'),
                            lazy='dynamic')

    @validates('eik_egn')
    def validate_eik_egn(self, key, value):
        assert (len(value) >= 9) & (len(value) <= 13)
        return value


class CounterpartyNote(BaseModel):
    __tablename__ = 'counterparty_notes'
    counterparty_id = Column(Integer(), ForeignKey('counterparties.id'))
    note = Column(UnicodeText(500), index=True)


class CounterpartyAccount(BaseModel):
    __tablename__ = 'counterparty_iban'
    counterparty_id = Column(Integer(), ForeignKey('counterparties.id'))
    iban = Column(String(22), index=True, unique=True)
    active = Column(Boolean(name='active_bool'), default=True, nullable=False)


counterparty_factory = functools.partial(model_factory, model=Counterparty)
counterparty_note_factory = functools.partial(model_factory,
                                              model=CounterpartyNote)
counterparty_account_factory = functools.partial(model_factory,
                                                 model=CounterpartyAccount)
