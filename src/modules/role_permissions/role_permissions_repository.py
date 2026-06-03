from modules.repository import Repository

from .role_permissions_entity import RolePermissionEntity
from ..permissions.permissions_entity import PermissionsEntity

class RolePermissionsRepository(Repository):
    
    def create_role_permission(self, role_permission_entity: RolePermissionEntity, session=None):
        return self.create_register_entity(role_permission_entity, session=session)
    
    def get_role_permission_by_id(self, id: int):
        return self.get_register_entity(RolePermissionEntity, id)
    
    def update_role_permission(self, role_permission_entity: RolePermissionEntity):
        return self.update_register_entity(role_permission_entity)

    def delete_role_permission(self, role_permission_entity: RolePermissionEntity):
        return self.delete_register_entity(role_permission_entity)

    def get_role_permission(self, role_id: int, permission_id: int) -> RolePermissionEntity | None:
        with self.get_session() as session:
            return session.query(
                RolePermissionEntity
            ).filter(
                RolePermissionEntity.role_id == role_id,
                RolePermissionEntity.permission_id == permission_id
            ).first()
    
    def get_all_permissions_by_role_id(self, role_id: int):
        with self.get_session() as session:
            results = session.query(
                PermissionsEntity.name
            ).join(
                RolePermissionEntity,
                PermissionsEntity.id == RolePermissionEntity.permission_id
            ).filter(
                RolePermissionEntity.role_id == role_id
            ).all()

            return [result.name for result in results]