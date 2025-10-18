from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional

class BaseProductModel(BaseModel):
    name: Optional[str] = Field(default=None, min_length=3, max_length=180, description="Name of the product")
    description: Optional[str] = Field(default=None, min_length=0, max_length=500, description="Description of the product")
    category_id: Optional[int] = Field(default=None, description="Id from the category")
    supplier_id: Optional[int] = Field(default=None, description="Id from the supplier")
    status: Optional[str] = Field(default="ACTIVE", description="Status of the product, defaults to 'ACTIVE'")
    date_creation: Optional[datetime] = Field(default_factory=datetime.now, description="Date of the creation product")
    date_updated: Optional[datetime] = Field(default_factory=datetime.now, description="Date of the last update from the product")

    @field_validator("*", mode="before")
    def convert_to_uppercase(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

    @field_validator("name")
    def name_must_contain_alphabet_characters(cls, value):
        if value and not any(str(c).isalpha() for c in value):
            raise ValueError("Name must contain alphabet characters.")
        return value

    @field_validator("category_id")
    def category_id_must_be_greater_than_0(cls, value):
        if value is not None and value < 0:
            raise ValueError("Category ID must be greater than 0.")
        return value

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {int: str}


class ProductModel(BaseProductModel):
    id: Optional[int] = Field(default=None, description="ID of the product")


class CreateProductModel(BaseProductModel):
    name: str
    description: str
    category_id: int
    supplier_id: Optional[int] = None


class UpdateProductModel(BaseProductModel):
    pass