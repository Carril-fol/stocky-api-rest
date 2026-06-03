from .user_repository import UserRepository
from .user_service import UserService
from ..roles.role_repository import RoleRepository
from ..users_companies.users_companies_repository import UsersCompaniesRepository
from ..role_permissions.role_permissions_repository import RolePermissionsRepository
from ..companies.company_repository import CompanyRepository
from ..permissions.permissions_repository import PermissionRepository

user_company_repo = UsersCompaniesRepository()
user_repository = UserRepository()
role_repository = RoleRepository()
role_permissions = RolePermissionsRepository()
company_repository = CompanyRepository()
permission_repository = PermissionRepository()

user_service = UserService(
    user_repository,
    user_company_repo,
    role_repository,
    role_permissions,
    company_repository,
    permission_repository
)