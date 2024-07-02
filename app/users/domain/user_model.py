import re
from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator

class UserModel(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    is_authenticated: bool = False
    is_admin: bool = False
    is_superuser: bool = False
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserModelRegister(UserModel):
    confirm_password: str

    @field_validator("password")
    def validation_passwords(cls, value):
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise Exception("Password must contain at least one special character.")
        return value
    
    @field_validator("confirm_password")
    def validation_passwords_match(cls, value):
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise Exception("Confirm password must contain at least one special character.")
        return value
    
    @field_validator("first_name", "last_name")
    def validation_first_name_and_last_name(cls, value):
        list_of_names = (str(value)).strip().split()
        capitalized_names = [name.capitalize() for name in list_of_names]
        long_name = " ".join(capitalized_names)
        return long_name