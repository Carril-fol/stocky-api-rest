from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserModel(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    firstName: str
    lastName: str
    email: EmailStr
    password: str
    isAuthenticated: bool = False
    isAdmin: bool = False
    isSuperUser: bool = False

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}