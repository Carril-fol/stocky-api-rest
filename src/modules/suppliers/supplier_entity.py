from core.database import Base
from ..companies.company_entity import CompanyEntity

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class SupplierEntity(Base):
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    status = Column(String, unique=False)
    company_id = Column(Integer, ForeignKey('companies.id'), nullable=False)
    
    companies = relationship(CompanyEntity)

    def to_dict(self):
        return { "id": self.id, "name": self.name, "status": self.status, "company_id": self.company_id }