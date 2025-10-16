from sqlalchemy import Column, Integer, String
from database.db import Base

class SupplierEntity(Base):
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    status = Column(String, unique=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status
        }