from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class ProductModel(BaseModel):
    id: Optional[int] = Field(default=None, description='ID of the product')
    name: Optional[str] = Field(default=None, min_length=3, max_length=50, description='Name of the product')
    description: Optional[str] = Field(default=None, min_length=3, max_length=300, description='Description of the product')
    category_id: int = Field(default=None, description='Id from the category')
    status: Optional[str] = Field(default='active', description="Status of the product, defaults to 'active'")
    date_creation: Optional[datetime] = Field(default_factory=datetime.now, description='Date of the creation product')
    date_updated: Optional[datetime] = Field(default_factory=datetime.now, description='Date of the last update from the product')

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

    @field_validator('category_id')
    def category_id_must_be_greater_than_0(cls, value):
        if value < 0:
            raise ValueError('Id from category must be greater than 0.')
        return value
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {int: str}