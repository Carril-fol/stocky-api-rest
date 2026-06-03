from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator, model_validator

StatusType = Literal["ACTIVE", "INACTIVE"]

# --------------------------------------------------------
# Base
# --------------------------------------------------------

class BaseRoleModel(BaseModel):
    name: Optional[str] = Field(default=None, description="The name of the role")
    status: Optional[StatusType] = Field(default="ACTIVE", description="Role status")
    company_id: Optional[int] = Field(default=None, description="The ID of the associated company")

    @field_validator('name', mode='before')
    @classmethod
    def normalize_name(cls, value: str) -> str:
        if isinstance(value, str):
            return value.upper()
        return value


# --------------------------------------------------------
# Create
# --------------------------------------------------------

class CreateRoleModel(BaseRoleModel):
    name: str = Field(..., description="The name of the role (required)")
    company_id: int = Field(..., description="The ID of the associated company (required)")


class CreateRoleInput(BaseModel):
    name: str = Field(..., description="The name of the role")

    @field_validator('name', mode='before')
    @classmethod
    def normalize_name(cls, value: str) -> str:
        if isinstance(value, str):
            return value.upper()
        return value


class CreateRoleOutput(BaseModel):
    msg: str = Field(..., examples=["Role created successfully"])


# --------------------------------------------------------
# Update
# --------------------------------------------------------

class UpdateRoleInput(BaseModel):
    name: Optional[str] = Field(default=None, description="Updated role name")
    status: Optional[StatusType] = Field(default=None, description="Updated role status")

    @field_validator('name', mode='before')
    @classmethod
    def normalize_name(cls, value: str) -> str:
        if isinstance(value, str):
            return value.upper()
        return value

    @model_validator(mode='after')
    def at_least_one_field(self) -> 'UpdateRoleInput':
        if self.name is None and self.status is None:
            raise ValueError('At least one field must be provided for update')
        return self


class UpdateRoleModel(BaseRoleModel):
    pass


class UpdateRoleOutput(BaseModel):
    msg: str = Field(..., examples=["Role updated successfully"])


# --------------------------------------------------------
# Detail
# --------------------------------------------------------

class DetailRoleModel(BaseRoleModel):
    id: int = Field(..., description="Role ID")


class RoleListDetail(BaseModel):
    data: list[DetailRoleModel]
    total: int
    page: int
    per_page: int
    total_pages: int


# --------------------------------------------------------
# Assign role to user
# --------------------------------------------------------

class AssignRoleInput(BaseModel):
    user_id: int = Field(..., description="The ID of the user to assign the role to")
    role_id: int = Field(..., description="The ID of the role to assign")


class AssignRoleOutput(BaseModel):
    msg: str = Field(..., examples=["Role assigned successfully"])


# --------------------------------------------------------
# Delete Role model
# --------------------------------------------------------

class DeleteRoleOutput(BaseModel):
    msg: str = Field(..., examples=["Role deleted successfully"])


# --------------------------------------------------------
# Others
# --------------------------------------------------------

class ErrorOutput(BaseModel):
    error: str = Field(..., examples=["Resource not found"])