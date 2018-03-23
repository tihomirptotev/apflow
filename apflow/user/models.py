import bcrypt
from sqlalchemy import (
    Column,
    Integer,
    Text,
    ForeignKey,
    Table
)
from sqlalchemy.orm import relationship, backref
from apflow.models.meta import Base
from apflow.models.mixins import SurrogatePK


roles_users = Table('roles_users', Base.metadata,
                          Column('user_id', Integer, ForeignKey('users.id')),
                          Column('role_id', Integer, ForeignKey('roles.id'))
                          )

class User(SurrogatePK, Base):
    __tablename__ = 'users'

    username = Column(Text, nullable=False, unique=True, index=True)
    email = Column(Text, nullable=False, unique=True, index=True)
    password_hash = Column(Text)
    roles = relationship('Role', secondary=roles_users,
                         back_populates='users')

    @property
    def password(self):
        raise PermissionError

    @password.setter
    def password(self, pw):
        self.set_password(pw)

    def set_password(self, pw):
        pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        self.password_hash = pwhash.decode('utf8')

    def check_password(self, pw):
        if self.password_hash is not None:
            expected_hash = self.password_hash.encode('utf8')
            return bcrypt.checkpw(pw.encode('utf8'), expected_hash)
        return False


class Role(SurrogatePK, Base):

    __tablename__ = 'roles'
    name = Column(Text, unique=True, index=True)
    description = Column(Text)
    users = relationship('User', secondary=roles_users,
                         back_populates='roles')

