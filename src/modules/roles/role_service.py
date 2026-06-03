from math import ceil

from modules.service import BaseService

from .role_repository import RoleRepository
from .role_entity import RoleEntity
from .role_model import CreateRoleModel, DetailRoleModel, RoleListDetail
from .role_exceptions import RoleNotFound, RoleIsAlreadyInactive, UserNotInCompany, RoleNameReserved

from ..users_companies.users_companies_repository import UsersCompaniesRepository
from ..users_companies.users_companies_entity import UsersCompaniesEntity


RESERVED_ROLE_NAME = "DEFAULT"


class RoleService(BaseService):
    
    def __init__(
            self, 
            role_repository: RoleRepository,
            user_role_repository: UsersCompaniesRepository
        ):
        self._role_repository = role_repository
        self._user_role_repository = user_role_repository

    # --------------------------------------------------------
    # Private functions
    # --------------------------------------------------------

    def _format_role(self, role_entity: RoleEntity):
        return DetailRoleModel.model_validate(
            role_entity.to_dict()
        ).model_dump(by_alias=True)
    
    def _create_default_role(self, company_id: int) -> RoleEntity:
        data = {"name": RESERVED_ROLE_NAME, "company_id": company_id, "status": "ACTIVE"}
        role_entity = RoleEntity(**data)
        return self._role_repository.create_role(role_entity).id

    def _reassign_users_to_default_role(self, list_users: list[UsersCompaniesEntity], new_role_id: int):
        data = {"role_id": new_role_id}
        for user in list_users:
            user_updated = self._update_instance_entity(data, user)
            self._user_role_repository.update_user_company_role(user_updated)
    
    def _create_and_reassing_default_role(self, deleted_role_id: int, company_id: int):
        affected_users = self._user_role_repository.get_users_by_role_id(deleted_role_id)
        
        if not affected_users:
            return
        
        default_role = self._create_default_role(company_id)
        self._reassign_users_to_default_role(affected_users, default_role)

    # --------------------------------------------------------
    # Public functions
    # --------------------------------------------------------

    def create_role(self, data: dict, company_id: int) -> RoleEntity:
        if data.get("name", "").upper() == RESERVED_ROLE_NAME:
            raise RoleNameReserved()

        data["company_id"] = company_id

        role_data_validated = CreateRoleModel.model_validate(
            data
        ).model_dump()

        role_entity = RoleEntity(**role_data_validated)
        return self._role_repository.create_role(role_entity)
    
    def get_roles_from_company(self, company_id: int, page: int, per_page: int) -> RoleListDetail:        
        roles_raw, total = self._role_repository.get_roles_from_company_id(company_id, page, per_page)
        roles_formatted: list[DetailRoleModel] = [self._format_role(rol) for rol in roles_raw]
        
        return RoleListDetail(
            data=roles_formatted,
            total=total,
            page=page,
            per_page=per_page,
            total_pages=ceil(total / per_page) if total > 0 else 1
        )
    
    def get_role_by_id(self, id: int) -> DetailRoleModel:
        role_raw = self._role_repository.get_role_by_id(id)
        if not role_raw:
            raise RoleNotFound()

        return self._format_role(role_raw)
    
    def delete_soft_rol(self, id: int, data: dict):
        role_instance = self._role_repository.get_role_by_id(id)
        if not role_instance:
            raise RoleNotFound()
        
        if role_instance.status == "INACTIVE":
            raise RoleIsAlreadyInactive()

        role_updated = self._update_instance_entity(data, role_instance)
        role_deleted = self._role_repository.delete_logic_register_entity(role_updated)

        self._create_and_reassing_default_role(id, role_instance.company_id)
        return role_deleted

    def update_role(self, id: int, data: dict):
        role_instance = self._role_repository.get_role_by_id(id)
        if not role_instance:
            raise RoleNotFound()

        role_to_updated = self._update_instance_entity(data, role_instance)
        return self._role_repository.update_role(role_to_updated)

    def assign_role_to_user(self, user_id: int, role_id: int, company_id: int):
        membership = self._user_role_repository.get_user_company_role_by_user_id(user_id)
        if not membership or membership.company_id != company_id:
            raise UserNotInCompany()

        role = self._role_repository.get_role_by_id(role_id)
        if not role or role.company_id != company_id:
            raise RoleNotFound()

        membership_updated = self._update_instance_entity({"role_id": role_id}, membership)
        return self._user_role_repository.update_user_company_role(membership_updated)