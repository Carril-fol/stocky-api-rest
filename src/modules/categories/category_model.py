from pydantic import BaseModel, Field, field_validator
from typing import Optional

class CategoryModel(BaseModel):
    id: int = Field(default=None, description='ID of the category')
    name: str = Field(default=None, description='Name of the category')
    status: str = Field(default='ACTIVE', description="Status of the category, defaults to 'active'")
    company_id: int
    
    @field_validator('*', mode='before')
    def convert_to_uppercase(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

    @field_validator('name')
    def name_must_contain_alphabet_characters(cls, value):
        if not any((str(character)).isalpha() for character in value):
            raise ValueError('name must contain alphabet characters')
        return value

    @field_validator('status')
    def status_must_be_active_or_inactive(cls, value):
        if value not in ['ACTIVE', 'INACTIVE']:
            raise ValueError('status must be active or inactive')
        return value 


# --------------------------------------------------------
# Create Category Model
# --------------------------------------------------------

class CreateCategoryInput(BaseModel):
    name: str = Field(default=None, min_length=3, max_length=150, description='Name of the category')
    status: Optional[str] = Field(default='ACTIVE', description="Status of the category, defaults to 'active'")


class CreateCategoryOutput(BaseModel):
    msg: str = Field(default='Category created successfully', description='Message of the response')


class CreateCategoryModel(BaseModel):
    name: str = Field(default=None, min_length=3, max_length=150, description='Name of the category')
    status: Optional[str] = Field(default='ACTIVE', description="Status of the category, defaults to 'active'")
    company_id: int

    @field_validator('name', mode='before')
    def uppercase_name(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value


# --------------------------------------------------------
# Update Category Model
# --------------------------------------------------------

class UpdateCategoryInput(BaseModel):
    name: str = Field(default=None, min_length=3, max_length=150, description='Name of the category')
    status: Optional[str] = Field(default='ACTIVE', description="Status of the category, defaults to 'active'")


class UpdateCategoryOutput(BaseModel):
    msg: str = Field(default='Category updated successfully', description='Message of the response')


class UpdateCategoryModel(BaseModel):
    name: str = Field(default=None, min_length=3, max_length=150, description='Name of the category')
    status: Optional[str] = Field(default='ACTIVE', description="Status of the category, defaults to 'active'")
    company_id: int

    @field_validator('name', mode='before')
    def uppercase_name(cls, value):
        if isinstance(value, str):
            return value.upper()
        return value

# --------------------------------------------------------
# Delete Category Model
# --------------------------------------------------------

class DeleteCategoryOutput(BaseModel):
    msg: str = Field(default='Category deleted successfully', description='Message of the response')


# --------------------------------------------------------
# Detail Category Model
# --------------------------------------------------------

class DetailCategoryModel(CategoryModel):
    pass


class DetailCategoryResponse(BaseModel):
    category: DetailCategoryModel = Field(..., description='Category detail wrapped in the response envelope')


class ListDetailCategoryModel(BaseModel):
    categories: list[DetailCategoryModel] = Field(..., description='List of categories with detailed information')
    total: int = Field(..., description='Total number of categories')
    page: int = Field(..., description='Current page number')
    per_page: int = Field(..., description='Number of categories per page')
    total_pages: int = Field(..., description='Total number of pages')


# --------------------------------------------------------
# Other Model
# --------------------------------------------------------

class ErrorOutput(BaseModel):
    msg: str = Field(..., description='Error message')