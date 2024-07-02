from pydantic import BaseModel, Field, field_validator
from bson import ObjectId
from typing import Optional

class CategoryModel(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    name: str = Field(min_length=3)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):
        if str(value).isdigit():
            raise ValueError("Categories cannot only have numbers")   
        names_list = str(value).strip().split()
        capitalized_name = [
            name.capitalize() if name.lower() != "y" else name.lower()
            for name in names_list
        ]
        long_name = " ".join(capitalized_name)
        return long_name

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}