from core.database import Base

from ..companies.company_entity import CompanyEntity
from ..categories.category_entity import CategoryEntity

from datetime import datetime
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class ProductEntity(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, unique=False)
    date_creation = Column(DateTime, nullable=False, default=datetime.now)
    date_updated = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)

    category = relationship(CategoryEntity)
    companies = relationship(CompanyEntity)

    def to_dict(self):
        return {colum.name: getattr(self, colum.name) for colum in self.__table__.columns}