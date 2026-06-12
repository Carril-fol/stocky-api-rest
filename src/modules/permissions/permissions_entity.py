from core.database import Base

from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

class PermissionsEntity(Base):
    __tablename__ = "permissions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
        }