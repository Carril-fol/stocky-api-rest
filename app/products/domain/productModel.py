from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional

class ProductModel(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    nameProduct: str
    quantityProduct: int

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}