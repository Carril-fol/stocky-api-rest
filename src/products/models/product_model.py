from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, field_validator

class ProductModel(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    name_product: str = Field(min_length=2)
    quantity_product: int
    price: int
    category_id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="category_id")

    @field_validator("name_product")
    def valid_name_product(cls, value):
        names_product = (str(value)).strip().split()
        capitalized_names = [name.capitalize() for name in names_product]
        long_name = " ".join(capitalized_names)
        return long_name
    
    @field_validator("quantity_product")
    def valid_quantity_product(cls, value):
        if value <= 0:
            raise ValueError("The quantity of the product cannot be less than 0")
        return value
    
    @field_validator("price")
    def valid_price(cls, value):
        if value <= 0:
            raise ValueError("The price of the product cannot be less or equals than 0")
        return value

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
