from core.database import Base
from ..users.user_entity import UserEntity
from ..roles.role_entity import RoleEntity
from ..companies.company_entity import CompanyEntity

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class UsersCompaniesEntity(Base):
    __tablename__ = "users_companies"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'),  nullable=False)
    
    roles = relationship(RoleEntity)
    users = relationship(UserEntity)
    companies = relationship(CompanyEntity)

    def to_dict(self):
        return {colum.name: getattr(self, colum.name) for colum in self.__table__.columns}