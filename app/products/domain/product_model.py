from datetime import date
from pydantic import BaseModel, Field, field_validator
from bson import ObjectId
from typing import Optional

class ProductModel(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    name_product: str = Field(min_length=2)
    quantity_product: int
    price: int
    category_id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="category_id")
    date_submited: date  = Field(default=date.today())
    date_updated: date = Field(default=None)

    @field_validator("name_product")
    def valid_name_product(cls, value):
        names_product = (str(value)).strip().split()
        capitalized_names = [name.capitalize() for name in names_product]
        long_name = " ".join(capitalized_names)
        return long_name
    
    @field_validator("quantity_product")
    def valid_quantity_product(cls, value):
        if value < 0:
            raise ValueError("The quantity of the product cannot be less than 0")
        return value
    
    @field_validator("price")
    def valid_price(cls, value):
        if value <= 0:
            raise ValueError("The price of the product cannot be less or equals than 0")
        return value
    
    @field_validator("date_submited")
    def valid_date_submited(cls, value):
        date_today = date.today()
        if value != date_today:
            raise ValueError(f"You cannot enter an upload date less than today: {date_today}")
        return value

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
