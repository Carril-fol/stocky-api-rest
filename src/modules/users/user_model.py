from datetime import datetime
from typing import Optional
from argon2 import PasswordHasher
from pydantic import BaseModel, Field, field_validator, model_validator
from .user_exceptions import EmailInvalidFormat, PasswordDontMatch
from ..companies.company_model import CreateCompanyInput

ph = PasswordHasher()

# --------------------------------------------------------
# Base Model
# --------------------------------------------------------

class BaseUserModel(BaseModel):
    first_name: str = Field(default=None, description='First name of the user')
    last_name: str = Field(default=None, description='Last name of the user')
    email: str = Field(default=None, description='Email of the user')
    date_creation: datetime = Field(default_factory=datetime.now, description="Date of the creation user")

    @field_validator("first_name", "last_name", mode='before',)
    def convert_to_uppercase(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value
    
    
# --------------------------------------------------------
# Create Model
# --------------------------------------------------------

class CreateUserModel(BaseUserModel):
    password: str = Field(...)

    @field_validator('password', mode='before')
    def hash_password(cls, value):
        return ph.hash(value)

    
# --------------------------------------------------------
# Update Model
# --------------------------------------------------------

class UpdateUserInput(BaseUserModel):
    password: str = Field(default=None)
    confirm_password: str = Field(default=None)

    @model_validator(mode='before')
    def check_passwords_match(cls, values):
        pw = values.get('password')
        cpw = values.get('confirm_password')
        if pw and cpw and pw != cpw:
            raise PasswordDontMatch()
        return values


class UpdateUserOutput(BaseModel):
    msg: str = Field(..., examples=["User updated successful"])


class UpdateUserModel(BaseModel):
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    email: Optional[str] = Field(default=None)
    password: Optional[str] = Field(default=None)

    @field_validator('password', mode='before')
    def hash_password(cls, value):
        if value:
            return ph.hash(value)
        return value


# --------------------------------------------------------
# Detail Model
# --------------------------------------------------------

class DetailUserModel(BaseUserModel):
    id: int = Field(..., description='ID of the user')
    date_creation: datetime = Field(..., description='Creation date of the user')


# --------------------------------------------------------
# Login Model
# --------------------------------------------------------

class LoginInput(BaseModel):
    email: str = Field(..., description="Email from user", examples=["example@example.com"])
    password: str = Field(..., min_length=1, description="Password in text plain")


class LoginOutput(BaseModel):
    msg: str = Field(..., examples=["Login successful"])


# --------------------------------------------------------
# Register Model
# --------------------------------------------------------

class RegisterInput(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: str = Field(...)
    password: str = Field(...)
    confirm_password: str = Field(...)

    @model_validator(mode='before')
    def check_passwords_match(cls, values):
        if values.get('password') != values.get('confirm_password'):
            raise PasswordDontMatch()
        return values
    
    @field_validator("email")
    def validate_email_format(cls, value):
        if "@" not in value or "." not in value:
            raise EmailInvalidFormat()
        return value


class RegisterOutput(BaseModel):
    msg: str = Field(..., examples=["Register successful"])


# --------------------------------------------------------
# Register User + Company
# --------------------------------------------------------

class RegisterWithCompanyInput(BaseModel):
    user: RegisterInput = Field(..., description="Datos del usuario OWNER")
    company: CreateCompanyInput = Field(..., description="Datos de la empresa")


# --------------------------------------------------------
# Register User for Company Models
# --------------------------------------------------------

class RegisterInputFromCompany(RegisterInput):
    role_id: int = Field(..., description="Role to assign to the new user")


class CreateUserFromCompany(CreateUserModel):
    pass


# --------------------------------------------------------
# Delete User model
# --------------------------------------------------------

class DeleteUserOutput(BaseModel):
    msg: str = Field(..., examples=["User deleted successfully"])


# --------------------------------------------------------
# Other Models
# --------------------------------------------------------

class ErrorOutput(BaseModel):
    error: str