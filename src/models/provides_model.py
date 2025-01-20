from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, field_validator

class ProvidesModel(BaseModel):
    product_id: int = Field(default=None, description='ID from the product')
    supplier_id: int = Field(default=None, description='ID from the supplier')
    entry_date: Optional[datetime] = Field(default=datetime.now(), description='Time when enter the product')

    @field_validator('product_id', 'supplier_id')
    def id_higher_to_zero(cls, value):
        if value < 0:
            raise ValueError()
        return value
