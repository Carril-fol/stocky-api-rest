from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class StockModel(BaseModel):
    id: Optional[int] = Field(default=None, description='ID of the stock')
    product_id: int = Field(default=None, description='FK of the product')
    quatity: int = Field(default=0, description='Quantity of the product')
    date_updated: Optional[datetime] = Field(default_factory=datetime.now, description='Date of the last update from the stock')
    