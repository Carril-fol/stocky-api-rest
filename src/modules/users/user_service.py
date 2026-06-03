from argon2 import PasswordHasher
from modules.service import BaseService
from core.database import Database

from .user_entity import UserEntity
from .user_repository import UserRepository
from .user_model import (
    CreateUserModel,
    DetailUserModel,
    UpdateUserModel,
    CreateUserFromCompany
)
from .user_exceptions import (
    UserNotFound,
    UserWithAnEmailAlreadyExists,
    PasswordDontMatch,
)

from ..roles.role_repository import RoleRepository
from ..roles.role_model import DetailRoleModel, CreateRoleModel
from ..roles.role_entity import RoleEntity

from ..users_companies.users_companies_entity import UsersCompaniesEntity
from ..users_companies.users_companies_repository import UsersCompaniesRepository
from ..users_companies.users_companies_model import DetailUsersCompaniesModel

from ..role_permissions.role_permissions_repository import RolePermissionsRepository
from ..role_permissions.role_permissions_entity import RolePermissionEntity

from ..companies.company_repository import CompanyRepository
from ..companies.company_entity import CompanyEntity
from ..companies.company_model import CreateCompanyModel

from ..permissions.permissions_repository import PermissionRepository
from ..permissions.permissions_exceptions import InsufficientRolePrivileges


ph = PasswordHasher()


class UserService(BaseService):

    def __init__(
            self,
            user_repository: UserRepository,
            users_companies_repo: UsersCompaniesRepository,
            role_repository: RoleRepository,
            _role_permissions_repo: RolePermissionsRepository,
            company_repository: CompanyRepository,
            permission_repository: PermissionRepository
        ):
        self.user_repository = user_repository
        self.users_companies_repo = users_companies_repo
        self._role_repository = role_repository
        self._role_permissions_repo = _role_permissions_repo
        self._company_repository = company_repository
        self._permission_repository = permission_repository

    # --------------------------------------------------------
    # Private functions
    # --------------------------------------------------------
    
    def _get_user_or_raise(self, user_id: int) -> UserEntity:
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFound()
        return user
     
    def _format_user(self, user_entity: UserEntity) -> dict:
        return DetailUserModel.model_validate(
            user_entity.to_dict()
        ).model_dump()

    def _verify_password(self, hashed: str, plain: str):
        if not ph.verify(hashed, plain):
            raise PasswordDontMatch()

    def _build_user_role_payload(self, user_company_role: UsersCompaniesEntity) -> dict:
        role_instance = self._role_repository.get_role_by_id(
            user_company_role.role_id
        )
        
        user_company_role_formatted = DetailUsersCompaniesModel.model_validate(
            user_company_role.to_dict()
        ).model_dump(exclude={"user_id"})

        role_formatted = DetailRoleModel.model_validate(
            role_instance.to_dict()
        ).model_dump(exclude={"company_id", "status"})

        return {
            **user_company_role_formatted,
            **role_formatted
        }

    def _validate_role_action(self, user_id: int, requesting_user_id: int, action: str) -> UsersCompaniesEntity:
        target_user_role = self.users_companies_repo.get_user_company_role_by_user_id(user_id)
        if target_user_role is None:
            raise UserNotFound()

        role_from_target_user = self._role_repository.get_role_by_id(target_user_role.role_id)
        requesting_user_role = self.users_companies_repo.get_user_company_role_by_user_id(requesting_user_id)

        if target_user_role.role_id == requesting_user_role.role_id:
            raise InsufficientRolePrivileges(f"You cannot {action} a user with the same role as you")

        if role_from_target_user.name == "OWNER":
            raise InsufficientRolePrivileges(f"Only users with OWNER role can {action} another OWNER user")

        return target_user_role

    # --------------------------------------------------------
    # Public functions
    # --------------------------------------------------------
     
    def register_owner(self, user_data: dict, company_data: dict) -> dict:
        if self.user_repository.get_user_by_email(user_data["email"]):
            raise UserWithAnEmailAlreadyExists()

        user_dump = CreateUserModel.model_validate(
            user_data
        ).model_dump(exclude={"confirm_password"})

        company_dump = CreateCompanyModel.model_validate(
            company_data
        ).model_dump()

        permissions = self._permission_repository.get_all_permissions()

        user_entity = UserEntity(**user_dump)
        company_entity = CompanyEntity(**company_dump)

        with self.user_repository.get_session() as session:
            self.user_repository.create_register_entity(user_entity, session=session)
            self._company_repository.create_register_entity(company_entity, session=session)

            role_dump = CreateRoleModel.model_validate(
                {"name": "OWNER", "company_id": company_entity.id}
            ).model_dump()
            role_entity = RoleEntity(**role_dump)
            self._role_repository.create_register_entity(role_entity, session=session)

            for permission in permissions:
                self._role_permissions_repo.create_register_entity(
                    RolePermissionEntity(
                        role_id=role_entity.id, 
                        permission_id=permission.id
                    ),
                    session=session
                )

            users_companies_entity = UsersCompaniesEntity(
                user_id=user_entity.id,
                role_id=role_entity.id,
                company_id=company_entity.id,
            )
            self.users_companies_repo.create_register_entity(
                users_companies_entity, session=session
            )

        return user_entity.id

    def update_user(self, user_id: int, user_data: dict) -> UserEntity:
        user = self._get_user_or_raise(user_id)
        
        user_update_model_data = UpdateUserModel.model_validate(
            user_data
        ).model_dump(exclude_unset=True)
        
        user_to_update = self._update_instance_entity(user_update_model_data, user)
        return self.user_repository.update_user(user_to_update)
    
    def get_user_by_id(self, user_id: int) -> dict:
        user = self._get_user_or_raise(user_id)
        return self._format_user(user)
    
    def authenticate_user(self, data: dict) -> dict:
        user = self.user_repository.get_user_by_email(data.get("email"))
        if not user:
            raise UserNotFound()

        self._verify_password(user.password, data.get("password"))

        return user.id

    def delete_user(self, user_id: int) -> None:
        user = self._get_user_or_raise(user_id)
        return self.user_repository.delete_user(user)

    def create_user_for_company(self, data: dict, company_id: int) -> None:
        if self.user_repository.get_user_by_email(data.get("email")):
            raise UserWithAnEmailAlreadyExists()

        user_model_create = CreateUserFromCompany.model_validate(
            data
        ).model_dump(exclude={"role_id"})

        user_entity = UserEntity(**user_model_create)

        with self.user_repository.get_session() as session:
            self.user_repository.create_user(user_entity, session=session)

            users_companies_entity = UsersCompaniesEntity(
                role_id=data["role_id"],
                user_id=user_entity.id,
                company_id=company_id,
            )
            self.users_companies_repo.create_user_company_role(
                users_companies_entity, session=session
            )

    def update_user_from_company(self, user_id: int, data: dict, requesting_user_id: int):
        self._validate_role_action(user_id, requesting_user_id, action="update")
        return self.update_user(user_id, data)

    def delete_user_from_company(self, user_id: int, requesting_user_id: int):
        target_user_role = self._validate_role_action(user_id, requesting_user_id, action="delete")
        self.users_companies_repo.delete_user_company_role(target_user_role)
        user_instance = self._get_user_or_raise(user_id)
        return self.user_repository.delete_user(user_instance)

    def get_users_from_company(self, company_id: int) -> list[dict]:
        memberships = self.users_companies_repo.get_users_by_company_id(company_id)
        return [self._format_user(self._get_user_or_raise(m.user_id)) for m in memberships]