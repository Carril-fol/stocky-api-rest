import pytest

from modules.users.user_orchestrator import user_service
from modules.companies.company_orchestrator import company_service

from modules.permissions.permissions_exceptions import InsufficientRolePrivileges
from modules.users_companies.users_companies_repository import UsersCompaniesRepository

from modules.roles.role_entity import RoleEntity
from modules.roles.role_repository import RoleRepository

users_companies_repo = UsersCompaniesRepository()
role_repo = RoleRepository()

# --------------------------------------------------------
# Data
# --------------------------------------------------------

USER_DATA = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@test.com",
    "password": "SecurePass123!",
    "confirm_password": "SecurePass123!",
}

COMPANY_DATA = {
    "name": "Test Corp",
    "country": "Argentina",
    "address": "123 Main St",
}

# --------------------------------------------------------
# Helpers
# --------------------------------------------------------

def _register_owner(user_data: dict, company_data: dict):
    user_id = user_service.register_owner(user_data, company_data)
    users_companies_data = users_companies_repo.get_user_company_role_by_user_id(user_id)
    return user_id, users_companies_data.company_id, users_companies_data.role_id

def _create_role(data: dict):
    role_entity = RoleEntity(**data)
    role_created = role_repo.create_role(role_entity)
    return role_created

def _register_worker(user_data: dict, role_id, company_id: int):
    user_data["role_id"] = role_id
    user_service.create_user_for_company(user_data, company_id)


# --------------------------------------------------------
# Update
# --------------------------------------------------------

def test_update_company_success():
    _, company_id, role_id = _register_owner(USER_DATA, COMPANY_DATA)
    update_company = company_service.update_company(
        company_id, 
        {**COMPANY_DATA, "name": "Test Corp Updated"},
        role_id
    )

    assert update_company is not None
    assert update_company.name == "Test Corp Updated"


def test_update_company_insufficient_privileges():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    role_created = _create_role({"name": "Role Test", "company_id": company_id})
    with pytest.raises(InsufficientRolePrivileges):
        company_service.update_company(
            company_id, 
            {**COMPANY_DATA, "name": "Test Corp Updated"},
            role_created.id
        )


# --------------------------------------------------------
# Detail
# --------------------------------------------------------

def test_detail_company_success():
    _, company_id, role_id = _register_owner(USER_DATA, COMPANY_DATA)
    company = company_service.detail_company(company_id, role_id)
    assert company["name"] == "TEST CORP" 