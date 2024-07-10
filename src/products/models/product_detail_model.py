from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field, field_validator

class ProductDetailModel(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    product_id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="product_id")
    barcode: str
    status: str

    @field_validator("barcode")
    def valid_barcode(cls, value):
        barcode = str(value)
        if not len(barcode) < 13 or len(barcode) > 13:
            raise Exception("The length of the barcode cannot be greater or less than 13 characters")
        if not barcode.isdigit():
            raise Exception("The barcode must contain numbers for identification")
        return value

    @field_validator("status")
    def valid_status(cls, value):
        status = str(value).lower()
        status_valids = ["available", "not available"]
        if not status in status_valids:
            raise Exception("The entered status is not available")
        return status

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}