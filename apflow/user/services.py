from sqlalchemy.orm.exc import NoResultFound
from apflow.services.base_services import ModelService
from .models import User, Role
from .schemas import UserSchema, RoleSchema

class UserService(ModelService):
    class Meta:
        model = User
        schema = UserSchema
        route_view_name = 'user_view'

    def get_by_identity(self, identity):
        """ Finds user by username or email """
        # session = self.request.dbsession
        try:
            user = self.find_by_col_name('username', identity).one()
            return user
        except NoResultFound:
            try:
                user = self.find_by_col_name('email', identity).one()
                return user
            except NoResultFound:
                return dict(
                    result='error',
                    message=f'Object with selected identity not found.')

    def assign_role_to_user(self, identity, role_name):
        user = self.get_by_identity(identity)
        role_service = RoleService(self.request)
        role = role_service.find_by_col_name('name', role_name).one()
        if isinstance(user, User) and isinstance(role, Role):
            user.roles.append(role)
            self.request.dbsession.add(user)
            self.request.dbsession.flush()
            return user

    def authenticate(self, identity, password):
        user = self.get_by_identity(identity)
        if isinstance(user, User) and user.check_password(password):
            return dict(
                userid=user.id,
                username=user.username,
                roles=[role.name for role in user.roles]
            )
        return None


class RoleService(ModelService):
    class Meta:
        model = Role
        schema = RoleSchema
        route_view_name = 'role_view'
