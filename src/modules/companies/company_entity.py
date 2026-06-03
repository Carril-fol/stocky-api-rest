from core.database import Base
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime

class CompanyEntity(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    address = Column(String, nullable=False)
    date_creation = Column(DateTime, nullable=False, default=datetime.now)
    
    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}