from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import Optional

class SupplierModel(BaseModel):
    id: int = Field(description='ID of the supplier')
    name: str = Field(min_length=3, max_length=50, description='Name of the supplier')
    status: str = Field(default='ACTIVE', description="Status of the supplier, defaults to 'active'")
    company_id: int = Field(description="Id from the company")

    @field_validator('*', mode='before')
    def convert_to_uppercase(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

    @field_validator('name')
    def name_must_contain_alphabet_characters(cls, value: str):
        if not any(character.isalpha() for character in value):
            raise ValueError('name must contain alphabet characters')
        return value

    @field_validator('status')
    def status_must_be_active_or_inactive(cls, value: str):
        if value not in ['ACTIVE', 'INACTIVE']:
            raise ValueError("status must be active or inactive")
        return value


# --------------------------------------------------------
# Create
# --------------------------------------------------------

class CreateSupplierInput(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    status: str = Field(..., description="Status of the supplier")


class CreateSupplierModel(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    status: str = Field(..., description="Status of the supplier")
    company_id: Optional[int] = Field(default=None)

    @field_validator('company_id', mode='before')
    def set_company_id(cls, value, info: ValidationInfo):
        if value is None and info.context:
            return info.context.get('company_id')
        return value


# --------------------------------------------------------
# Update
# --------------------------------------------------------

class UpdateSupplierInput(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    status: str = Field(..., description="Status of the supplier")


class UpdateSupplierModel(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    status: str = Field(..., description="Status of the supplier")
    company_id: Optional[int] = Field(default=None)

    @field_validator('company_id', mode='before')
    def set_company_id(cls, value, info: ValidationInfo):
        if value is None and info.context:
            return info.context.get('company_id')
        return value


# --------------------------------------------------------
# Detail
# --------------------------------------------------------

class SupplierDetailOutput(BaseModel):
    supplier: SupplierModel


class SupplierListOutput(BaseModel):
    suppliers: list[SupplierModel]


# --------------------------------------------------------
# Other responses
# --------------------------------------------------------

class ErrorOutput(BaseModel):
    error: str

class SupplierCreatedOutput(BaseModel):
    msg: str = Field(..., examples=["Supplier created successfully"])

class SupplierUpdatedOutput(BaseModel):
    msg: str = Field(..., examples=["Supplier updated successfully"])

class SupplierDeletedOutput(BaseModel):
    msg: str = Field(..., examples=["Supplier deleted successfully"])