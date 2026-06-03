from modules.service import BaseService

from ..roles.role_repository import RoleRepository
from .role_permissions_repository import RolePermissionsRepository
from .role_permissions_entity import RolePermissionEntity
from .role_permission_model import (
    AssignRolePermissionModel,
    UpdateRolePermissionModel
)
from .role_permission_exceptions import (
    RoleNotInCompany, 
    RolePermissionNotFound, 
    RolePermissionsAlreadyHasAPermission
)

class RolePermissionService(BaseService):
    
    def __init__(
        self,
        role_permission_repo: RolePermissionsRepository,
        role_repo: RoleRepository
    ):
        self._role_permission_repo = role_permission_repo
        self._role_repo = role_repo

    # --------------------------------------------------------
    # Private functions
    # --------------------------------------------------------

    def _get_role_permission_by_id(self, id: int):
        return self._role_permission_repo.get_role_permission_by_id(id)

    def _get_company_role_or_raise(self, role_id: int, company_id: int):
        role = self._role_repo.get_role_by_id(role_id)
        if not role or role.company_id != company_id:
            raise RoleNotInCompany()

        return role

    # --------------------------------------------------------
    # Public functions
    # --------------------------------------------------------

    def role_has_permission(self, role_id: int, permission_id: int):
        return self._role_permission_repo.get_role_permission(role_id, permission_id)

    def assign_role_permission_service(self, data: dict, company_id: int):
        assign_role_permission = AssignRolePermissionModel.model_validate(data)
        role_id = assign_role_permission.role_id
        permission_ids = assign_role_permission.permission_id

        self._get_company_role_or_raise(role_id, company_id)

        for permission_id in permission_ids:
            already_exists = self._role_permission_repo.get_role_permission(role_id, permission_id)
            if already_exists:
                raise RolePermissionsAlreadyHasAPermission()

            role_permission_entity = RolePermissionEntity(
                role_id=role_id,
                permission_id=permission_id
            )
            self._role_permission_repo.create_role_permission(role_permission_entity)

    def update_role_permission_service(self, id: int, data: dict, company_id: int):
        role_permission = self._get_role_permission_by_id(id)
        if not role_permission:
            raise RolePermissionNotFound()

        self._get_company_role_or_raise(role_permission.role_id, company_id)

        data_validated = UpdateRolePermissionModel.model_validate(
            data
        ).model_dump()

        self._get_company_role_or_raise(data_validated["role_id"], company_id)

        role_permission_updated = self._update_instance_entity(data_validated, role_permission)
        return self._role_permission_repo.update_role_permission(role_permission_updated)
    
    def list_permissions_by_role_id(self, role_id: int, company_id: int) -> list[str]:
        self._get_company_role_or_raise(role_id, company_id)
        return self._role_permission_repo.get_all_permissions_by_role_id(role_id)

    def revoke_permission(self, role_id: int, permission_id: int, company_id: int):
        self._get_company_role_or_raise(role_id, company_id)
        link = self._role_permission_repo.get_role_permission(role_id, permission_id)
        if not link:
            raise RolePermissionNotFound()
        
        return self._role_permission_repo.delete_role_permission(link)