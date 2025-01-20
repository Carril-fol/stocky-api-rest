from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database.db import Base
from product_entity import ProductEntity

class StockEntity(Base):
    __tablename__ = 'stock'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    date_updated = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())
    products = relationship(ProductEntity)
