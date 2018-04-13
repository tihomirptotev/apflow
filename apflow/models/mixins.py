import arrow
from sqlalchemy import Column, Integer, Boolean
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
    # Column for soft delete
    deleted = Column(Boolean(name='deleted_bool'), default=False)


class CRUDMixin:

    def save(self, dbsession):
        dbsession.add(self)
        dbsession.flush()
        return self

    def update(self, **data):
        for k, v in data.items():
            setattr(self, k, v)
        return self

    def delete(self, dbsession):
        dbsession.delete(self)
        dbsession.flush()

    @classmethod
    def get_by_id(cls, dbsession, id):
        """Get record by ID."""
        return dbsession.query(cls).filter_by(id=id).one()

    @classmethod
    def find_by_col_name(cls, dbsession, col_name, value):
        """Find record by column name."""
        col = getattr(cls, col_name)
        return dbsession.query(cls).filter(col==value).first()

    def serialize(self, schema):
        """ Serializes object with provided marshmallow schema. """
        return schema.dump(self)


class BaseModel(AuditMixin, CRUDMixin, Base):

    __abstract__ = True
