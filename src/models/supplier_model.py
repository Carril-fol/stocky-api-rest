from pydantic import BaseModel, Field, field_validator
from typing import Optional

class SupplierModel(BaseModel):
    id: int = Field(default=None, description='ID of the supplier')
    name: str = Field(default=None, min_length=3, max_length=50, description='Name of the supplier')
    status: str = Field(default='ACTIVE', description="Status of the supplier, defaults to 'active'")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {int: str}


class CreateUpdateSupplierModel(BaseModel):
    name: str = Field(default=None, min_length=3, max_length=120, description='Name of the supplier')
    status: Optional[str] = Field(default='ACTIVE', description="Status of the supplier, defaults to 'active'")

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