from modules.service import BaseService

from .company_repository import CompanyRepository
from .company_model import DetailCompanyModel
from .company_entity import CompanyEntity
from .company_exceptions import CompanyNotFound

from ..roles.role_repository import RoleRepository
from ..permissions.permissions_exceptions import InsufficientRolePrivileges


class CompanyService(BaseService):

    def __init__(
            self, 
            company_repository: CompanyRepository, 
            role_repository: RoleRepository, 
        ):
        self.company_repository = company_repository
        self._role_repository = role_repository

    # --------------------------------------------------------
    # Private functions
    # --------------------------------------------------------

    def _format_company(self, company_entity: CompanyEntity):
        return DetailCompanyModel.model_validate(
            company_entity.to_dict()
        ).model_dump(by_alias=True)

    def _is_user_owner_of_company_or_from_company(self, requesting_role_id: int, company_id: int) -> bool:
        requesting_role = self._role_repository.get_role_by_id(requesting_role_id)
        if requesting_role.company_id != company_id:
            return False
        
        if requesting_role.name == "OWNER" and requesting_role.company_id == company_id:
            return True
        
        return False
    
    def _get_company_or_raise(self, company_id: int) -> CompanyEntity:
        company = self.company_repository.get_company_by_id(company_id)
        if not company:
            raise CompanyNotFound()
        
        return company

    # --------------------------------------------------------
    # Public functions
    # --------------------------------------------------------

    def update_company(self, company_id: int, data: dict, requesting_role_id: int) -> CompanyEntity:
        if not self._is_user_owner_of_company_or_from_company(requesting_role_id, company_id):
            raise InsufficientRolePrivileges()
        
        company_instance = self._get_company_or_raise(company_id)
        company_updated = self._update_instance_entity(data, company_instance)
        return self.company_repository.update_company(company_updated)

    def detail_company(self, company_id: int, requesting_role_id: int) -> dict:
        if not self._is_user_owner_of_company_or_from_company(requesting_role_id, company_id):
            raise InsufficientRolePrivileges()

        company_instance = self._get_company_or_raise(company_id)
        return self._format_company(company_instance)