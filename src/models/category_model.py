from pydantic import BaseModel, Field, field_validator
from typing import Optional

class CategoryModel(BaseModel):
    id: int = Field(default=None, description='ID of the category')
    name: str = Field(default=None, description='Name of the category')
    status: str = Field(default='active', description="Status of the category, defaults to 'active'")
    
    @field_validator('*', mode='before')
    def convert_to_uppercase(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

    @field_validator('name')
    def name_must_contain_alphabet_characters(cls, value):
        if not any((str(character)).isalpha() for character in value):
            raise ValueError('name must contain alphabet characters')
        return value

    @field_validator('status')
    def status_must_be_active_or_inactive(cls, value):
        if value not in ['active', 'inactive']:
            raise ValueError('status must be active or inactive')
        return value 

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {int: str}


class CreateOrUpdateCategoryModel(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=150, description='Name of the category')
    status: Optional[str] = Field(default='active', description="Status of the category, defaults to 'active'")

    @field_validator('*', mode='before')
    def convert_to_uppercase(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

    @field_validator('name')
    def name_must_contain_alphabet_characters(cls, value):
        if not any((str(character)).isalpha() for character in value):
            raise ValueError('name must contain alphabet characters')
        return value

    @field_validator('status')
    def status_must_be_active_or_inactive(cls, value):
        if value not in ['ACTIVE', 'INACTIVE']:
            raise ValueError('status must be active or inactive')
        return value 

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {int: str}