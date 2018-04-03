import arrow
from sqlalchemy import Column, Integer
from sqlalchemy_utils import ArrowType
from apflow.models.meta import Base
import transaction


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


class CRUDMixin:

    @classmethod
    def get_by_id(cls, dbsession, id):
        """Get record by ID."""
        return dbsession.query(cls).filter_by(id=id).one()

    @classmethod
    def find_by_col_name(cls, dbsession, col_name, value):
        """Find record by column name."""
        col = getattr(cls, col_name)
        return dbsession.query(cls).filter(col==value)



class BaseModel(AuditMixin, CRUDMixin, Base):

    __abstract__ = True
