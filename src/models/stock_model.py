from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator

status_type = Literal['IN STOCK', 'LOW STOCK', 'OUT OF STOCK', 'INACTIVE']

class BaseStockModel(BaseModel):
    product_id: Optional[int] = Field(default=None, description='FK of the product')
    quantity: Optional[int] = Field(default=0, description='Quantity of the product')
    status: Optional[status_type] = Field(default='IN STOCK', description='Status of the stock')
    date_updated: Optional[datetime] = Field(default_factory=datetime.now, description='Date of the last update from the stock')
    
    @field_validator("*", mode="before")
    def convert_to_uppercase(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

    @field_validator('product_id')
    def validate_product_id(cls, value):
        if value is None:
            raise ValueError('Product ID is required')
        return value

    @field_validator('quantity')
    def quantity_has_to_be_higher_to_zero(cls, value):
        if value < 0:
            raise ValueError('Quantity has to be higher than zero')
        return value


class CreateStockModel(BaseStockModel):
    product_id: int
    quantity: int


class UpdateStockModel(BaseStockModel):
    pass


class StockDetail(BaseStockModel):
    id: int


class StockProductDetail(BaseModel):
    id: int = Field(default=None, description="Id from the stock")
    product_id: int = Field(default=None, description='Id from the product')
    quantity: int = Field(default=None, description='Number representation of the quantiy of a product')
    status: str = Field(default=None, description='Status from the stock')
    name: str = Field(default=None)
    description: str = Field(default=None)
    category_id: int = Field(default=None)
    date_updated: datetime = Field(default=None)
    date_creation: datetime = Field(default=None)