from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional


class BaseCompanyModel(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=255, description="Name of the company")
    address: Optional[str] = Field(default=None, min_length=5, max_length=255, description="Address of the company")
    country: Optional[str] = Field(default=None, min_length=2, max_length=100, description="Country of the company")
    date_creation: Optional[datetime] = Field(default=None, description="Date of the creation company")

    @field_validator("name", "address", "country", mode="before")
    @classmethod
    def convert_to_uppercase(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value


# --------------------------------------------------------
# Create Company Model
# --------------------------------------------------------

class CreateCompanyInput(BaseModel):
    name: str = Field(..., min_length=2, max_length=255, description="Name of the company")
    country: str = Field(..., min_length=2, max_length=100, description="Country of the company")
    address: Optional[str] = Field(default=None, min_length=5, max_length=255, description="Address of the company")


class CreateCompanyModel(BaseCompanyModel):
    name: str = Field(..., min_length=2, max_length=255)
    country: str = Field(..., min_length=2, max_length=100)
    date_creation: datetime = Field(default_factory=datetime.now)


class CreateCompanyOutput(BaseModel):
    msg: str = Field(..., description="Message of the create company", examples=["Company created successfully"])


# --------------------------------------------------------
# Update Company Model
# --------------------------------------------------------

class UpdateCompanyInput(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=255, description="Name of the company")
    address: Optional[str] = Field(default=None, min_length=5, max_length=255, description="Address of the company")
    country: Optional[str] = Field(default=None, min_length=2, max_length=100, description="Country of the company")


class UpdateCompanyOutput(BaseModel):
    msg: str = Field(..., description="Message of the update company", examples=["Company updated successfully"])


class UpdateCompanyModel(BaseCompanyModel):
    pass


# --------------------------------------------------------
# Detail Company Model
# --------------------------------------------------------

class DetailCompanyModel(BaseCompanyModel):
    id: int = Field(..., description="Id from company")


# --------------------------------------------------------
# Delete Company Model
# --------------------------------------------------------

class DeleteCompanyOutput(BaseModel):
    msg: str = Field(..., description="Message of the delete company", examples=["Company deleted successfully"])


# --------------------------------------------------------
# Error Model
# --------------------------------------------------------

class ErrorOutput(BaseModel):
    msg: str = Field(..., description='Error message')