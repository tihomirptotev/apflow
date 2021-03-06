import functools
import arrow
from passlib.apps import custom_app_context
from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
    Table,
    Boolean
)
from sqlalchemy import or_
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import relationship, backref
from sqlalchemy_utils import ArrowType
from apflow.models.meta import Base
from apflow.models.mixins import BaseModel
from apflow.views.base_api import model_factory


roles_users = Table('roles_users', Base.metadata,
                          Column('user_id', Integer, ForeignKey('users.id')),
                          Column('role_id', Integer, ForeignKey('roles.id')),
                          Column('created_by', Integer, default=1),
                          Column('updated_by', Integer, default=1),
                          Column('created_on', ArrowType, default=arrow.utcnow),
                          Column('updated_on', ArrowType,
                                 default=arrow.utcnow, onupdate=arrow.utcnow)
                          )

class User(BaseModel):
    __tablename__ = 'users'

    username = Column(Text, nullable=False, unique=True, index=True)
    email = Column(Text, nullable=False, unique=True, index=True)
    password_hash = Column(Text)
    roles = relationship('Role', secondary=roles_users,
                         back_populates='users')
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
    employee = relationship('Employee', back_populates='user')
    active = Column(Boolean(name='active_bool'), default=True)

    @property
    def password(self):
        raise PermissionError

    @password.setter
    def password(self, pw):
        self.set_password(pw)

    def set_password(self, pw):
        self.password_hash = custom_app_context.hash(pw)

    def check_password(self, pw):
        return custom_app_context.verify(pw, self.password_hash)

    @staticmethod
    def get_by_identity(identity, dbsession):
        """ Finds user by username or email """
        try:
            user = dbsession.query(User).filter(
                or_(User.username==identity, User.email==identity)
            ).first()
            return user
        except NoResultFound:
                return None

    @staticmethod
    def authenticate(identity, password, dbsession):
        """ Authenticates the user. """
        user = User.get_by_identity(identity, dbsession)
        if user and user.check_password(password):
            return dict(
                userid=user.id,
                username=user.username,
                email=user.email,
                roles=[role.name for role in user.roles]
            )
        return None


class Role(BaseModel):

    __tablename__ = 'roles'
    name = Column(Text, unique=True, index=True)
    description = Column(Text)
    users = relationship('User', secondary=roles_users,
                         back_populates='roles')
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)


user_factory = functools.partial(model_factory, model=User)
