from ..roles.role_repository import RoleRepository
from .company_repository import CompanyRepository
from .company_service import CompanyService

role_repository = RoleRepository()
company_repository = CompanyRepository()

company_service = CompanyService(
    company_repository, 
    role_repository, 
)