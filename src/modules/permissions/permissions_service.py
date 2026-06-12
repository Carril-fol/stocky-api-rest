from modules.service import BaseService

from .permissions_entity import PermissionsEntity
from .permissions_repository import PermissionRepository
from .permissions_models import (
    PermissionModel,
    CreatePermissionModel,
)
from .permissions_exceptions import (
    PermissionNotFound, 
    PermissionAlreadyExists
)


class PermissionService(BaseService):

    def __init__(self, permission_repo: PermissionRepository):
        self._permission_repo = permission_repo

    # --------------------------------------------------------
    # Private functions
    # --------------------------------------------------------

    def _get_permission_by_name(self, name: str) -> PermissionsEntity:
        permission_instance = self._permission_repo.get_permission_by_name(name)
        if not permission_instance:
            raise PermissionNotFound()
        return permission_instance

    # --------------------------------------------------------
    # Public functions
    # --------------------------------------------------------

    def get_permission_by_name(self, name: str) -> dict:
        permission_instance = self._get_permission_by_name(name)
        return PermissionModel.model_validate(
            permission_instance.to_dict()
        ).model_dump()

    def create_permission(self, data: dict):
        normalized_name = data["name"].upper()
        existing = self._permission_repo.get_permission_by_name(normalized_name)
        if existing:
            raise PermissionAlreadyExists()

        permission_data = CreatePermissionModel.model_validate(
            data
        ).model_dump()

        permission = PermissionsEntity(**permission_data)
        return self._permission_repo.create_permission(permission)