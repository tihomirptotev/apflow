from passlib.apps import custom_app_context
from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
    Table
)
from sqlalchemy.orm import relationship, backref
from apflow.models.meta import Base
from apflow.models.mixins import BaseModel


roles_users = Table('roles_users', Base.metadata,
                          Column('user_id', Integer, ForeignKey('users.id')),
                          Column('role_id', Integer, ForeignKey('roles.id'))
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


class Role(BaseModel):

    __tablename__ = 'roles'
    name = Column(Text, unique=True, index=True)
    description = Column(Text)
    users = relationship('User', secondary=roles_users,
                         back_populates='roles')
    created_by = Column(Integer, nullable=True)
    updated_by = Column(Integer, nullable=True)
