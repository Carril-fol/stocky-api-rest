from ..service import BaseService

from modules.users_companies.users_companies_model import CreateUserRoleModel
from modules.users_companies.users_companies_entity import UserRoleEntity
from modules.users_companies.users_companies_repository import UserRoleRepository

class UserRoleService(BaseService):
    
    def __init__(self, user_role_repository: UserRoleRepository):
        self.user_role_repository = user_role_repository
    
    def create_user_role(self, data: dict):
        validated_data = CreateUserRoleModel.model_validate(data).model_dump(by_alias=True)
        user_role_entity = UserRoleEntity(**validated_data)
        return self.user_role_repository.create_user_role(user_role_entity)
        