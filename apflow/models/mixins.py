import arrow
from sqlalchemy import Column, Integer
from sqlalchemy_utils import ArrowType


class SurrogatePK:
    """A mixin that adds a surrogate integer 'primary key' column
       named ``id`` to any declarative-mapped class."""

    # __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)

    # @classmethod
    # def get_by_id(cls, record_id):
    #     """Get record by ID."""
    #     if any(
    #             (isinstance(record_id, (bytes, str)) and record_id.isdigit(),
    #              isinstance(record_id, (int, float))),
    #     ):
    #         return cls.query.get(int(record_id))
    #     return None


class AuditMixin(SurrogatePK):

    created_on = Column(ArrowType, default=arrow.utcnow)
    updated_on = Column(ArrowType, default=arrow.utcnow, onupdate=arrow.utcnow)
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer, nullable=False)
