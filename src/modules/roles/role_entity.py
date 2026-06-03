from core.database import Base
from ..companies.company_entity import CompanyEntity

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class RoleEntity(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    status = Column(String)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    companies = relationship(CompanyEntity)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}