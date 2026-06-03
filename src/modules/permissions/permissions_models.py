from pydantic import BaseModel

class CRUDPermissionBase(BaseModel):
    name: str


class PermissionModel(CRUDPermissionBase):
    id: int


class UpdatePermissionModel(CRUDPermissionBase):
    pass


class CreatePermissionModel(CRUDPermissionBase):
    pass

