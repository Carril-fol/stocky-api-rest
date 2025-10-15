from sqlalchemy import Column, Integer, String
from database.db import Base

class CategoryEntity(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    status = Column(String, unique=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status
        }