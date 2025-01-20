from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from database.db import Base
from product_entity import ProductEntity
from supplier_entity import SupplierEntity

class ProvidesEntity(Base):
    __tablename__ = 'provides'
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=False)
    entry_date = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())
    products = relationship(ProductEntity)
    suppliers = relationship(SupplierEntity)