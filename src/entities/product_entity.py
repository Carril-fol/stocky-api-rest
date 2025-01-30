from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.db import Base
from .category_entity import CategoryEntity
from .supplier_entity import SupplierEntity

class ProductEntity(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    supplier_id = Column(Integer, ForeignKey('suppliers.id'), nullable=False)
    status = Column(String, unique=False)
    date_creation = Column(DateTime, nullable=False, default=datetime.now())
    date_updated = Column(DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())
    category = relationship(CategoryEntity)
    supplier = relationship(SupplierEntity)
