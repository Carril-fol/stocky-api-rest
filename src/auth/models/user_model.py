import re
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, field_validator

class UserModel(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    is_verfied: bool = False
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
        """
        This validation allows you to check if the password 
        contains special characters

        Args:
        ----
        value (str): Password introduced from the user

        Returns:
        -------
        value (str): Password introduced from the user
        """
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise Exception("Password must contain at least one special character.")
        return value
    
    @field_validator("confirm_password")
    def validation_passwords_match(cls, value):
        """
        This validation allows you to check if the 
        password contains special characters

        Args:
        ----
        value (str): Password introduced from the user

        Returns:
        -------
        value (str): Password introduced from the user
        """
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise Exception("Confirm password must contain at least one special character.")
        return value
    
    @field_validator("first_name", "last_name")
    def validation_first_name_and_last_name(cls, value):
        """
        This validation separates the names entered by users to 
        format them to lowercase and save them
        
        Args:
        ----
        value (str): first_name and last_name introduced from the user

        Returns:
        -------
        value (str): first_name and last_name introduced from the user
        """
        list_of_names = (str(value)).strip().split()
        capitalized_names = [name.lower() for name in list_of_names]
        long_name = " ".join(capitalized_names)
        return long_name
