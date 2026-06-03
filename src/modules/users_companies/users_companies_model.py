from pydantic import BaseModel, Field

from ..companies.company_model import CreateCompanyInput
from ..users.user_model import RegisterInput, CreateUserModel


class BaseUsersCompaniesModel(BaseModel):
    user_id: int
    role_id: int
    company_id: int

    
class CreateUsersCompaniesModel(BaseUsersCompaniesModel):
    pass


class DetailUsersCompaniesModel(BaseUsersCompaniesModel):
    pass


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