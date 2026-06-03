from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from core.database import Base
from ..roles.role_entity import RoleEntity
from ..permissions.permissions_entity import PermissionsEntity

class RolePermissionEntity(Base):
    __tablename__ = "role_permission"
    id = Column(Integer, primary_key=True, index=True)
    permission_id = Column(Integer, ForeignKey("permissions.id"), nullable=False)
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)

    permissions = relationship(PermissionsEntity)
    roles = relationship(RoleEntity)  

    def to_dict(self):
        return {
            "id": self.id,
            "permission_id": self.permission_id,
            "role_id": self.role_id
        }