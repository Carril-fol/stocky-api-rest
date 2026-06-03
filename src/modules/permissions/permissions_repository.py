from modules.repository import Repository
from .permissions_entity import PermissionsEntity


class PermissionRepository(Repository):

    def create_permission(self, permission_instance: PermissionsEntity):
        return self.create_register_entity(permission_instance)
    
    def get_permission_by_id(self, id: int) -> PermissionsEntity:
        return self.get_register_entity(PermissionsEntity, id)
    
    def get_permission_by_name(self, name: str) -> PermissionsEntity | None:
        with self.get_session() as session:
            return session.query(
                PermissionsEntity
            ).filter(
                PermissionsEntity.name == name
            ).first()

    def get_all_permissions(self) -> list[PermissionsEntity]:
        return self.get_registers_entity(PermissionsEntity)