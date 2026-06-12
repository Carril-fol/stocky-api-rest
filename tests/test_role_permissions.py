import pytest

from modules.users.user_orchestrator import user_service
from modules.users_companies.users_companies_repository import UsersCompaniesRepository
from modules.roles.role_repository import RoleRepository
from modules.roles.role_entity import RoleEntity
from modules.permissions.permissions_repository import PermissionRepository
from modules.role_permissions.role_permission_service import RolePermissionService
from modules.role_permissions.role_permissions_repository import RolePermissionsRepository
from modules.role_permissions.role_permission_exceptions import (
    RoleNotInCompany,
    RolePermissionNotFound,
    RolePermissionsAlreadyHasAPermission,
)

users_companies_repo = UsersCompaniesRepository()
role_repo = RoleRepository()
permission_repo = PermissionRepository()
role_permission_repo = RolePermissionsRepository()
role_permission_service = RolePermissionService(role_permission_repo, role_repo)

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
    uc = users_companies_repo.get_user_company_role_by_user_id(user_id)
    return user_id, uc.company_id, uc.role_id


def _create_role(name: str, company_id: int) -> RoleEntity:
    return role_repo.create_role(RoleEntity(name=name, company_id=company_id))


def _get_permission_id(name: str) -> int:
    return permission_repo.get_permission_by_name(name).id


def _assign(role_id: int, permission_id: int, company_id: int):
    role_permission_service.assign_role_permission_service(
        {"role_id": role_id, "permission_id": [permission_id]},
        company_id,
    )


# --------------------------------------------------------
# Assign
# --------------------------------------------------------

def test_assign_permission_success():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    role = _create_role("Manager", company_id)
    p_id = _get_permission_id("CREATE_USER")

    _assign(role.id, p_id, company_id)

    assert role_permission_service.role_has_permission(role.id, p_id) is not None


def test_assign_multiple_permissions_success():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    role = _create_role("Admin", company_id)
    p1 = _get_permission_id("CREATE_USER")
    p2 = _get_permission_id("READ_USER")

    role_permission_service.assign_role_permission_service(
        {"role_id": role.id, "permission_id": [p1, p2]},
        company_id,
    )

    permissions = role_permission_service.list_permissions_by_role_id(role.id, company_id)
    assert "CREATE_USER" in permissions
    assert "READ_USER" in permissions


def test_assign_permission_already_assigned():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    role = _create_role("Manager", company_id)
    p_id = _get_permission_id("CREATE_USER")
    _assign(role.id, p_id, company_id)

    with pytest.raises(RolePermissionsAlreadyHasAPermission):
        _assign(role.id, p_id, company_id)


def test_assign_permission_role_not_in_company():
    _, company_a_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    _, company_b_id, _ = _register_owner(
        {**USER_DATA, "email": "owner_b@test.com"},
        {**COMPANY_DATA, "name": "Company B"},
    )
    role_b = _create_role("Role B", company_b_id)
    p_id = _get_permission_id("CREATE_USER")

    with pytest.raises(RoleNotInCompany):
        _assign(role_b.id, p_id, company_a_id)


# --------------------------------------------------------
# List permissions by role
# --------------------------------------------------------

def test_list_permissions_success():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    role = _create_role("Manager", company_id)
    p_id = _get_permission_id("READ_STOCK")
    _assign(role.id, p_id, company_id)

    result = role_permission_service.list_permissions_by_role_id(role.id, company_id)

    assert "READ_STOCK" in result


def test_list_permissions_empty():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    role = _create_role("Empty Role", company_id)

    result = role_permission_service.list_permissions_by_role_id(role.id, company_id)

    assert result == []


def test_list_permissions_role_not_in_company():
    _, company_a_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    _, company_b_id, _ = _register_owner(
        {**USER_DATA, "email": "owner_b@test.com"},
        {**COMPANY_DATA, "name": "Company B"},
    )
    role_b = _create_role("Role B", company_b_id)

    with pytest.raises(RoleNotInCompany):
        role_permission_service.list_permissions_by_role_id(role_b.id, company_a_id)


# --------------------------------------------------------
# Revoke
# --------------------------------------------------------

def test_revoke_permission_success():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    role = _create_role("Manager", company_id)
    p_id = _get_permission_id("DELETE_USER")
    _assign(role.id, p_id, company_id)

    role_permission_service.revoke_permission(role.id, p_id, company_id)

    assert role_permission_service.role_has_permission(role.id, p_id) is None


def test_revoke_permission_not_assigned():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    role = _create_role("Manager", company_id)
    p_id = _get_permission_id("DELETE_USER")

    with pytest.raises(RolePermissionNotFound):
        role_permission_service.revoke_permission(role.id, p_id, company_id)


def test_revoke_permission_role_not_in_company():
    _, company_a_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    _, company_b_id, _ = _register_owner(
        {**USER_DATA, "email": "owner_b@test.com"},
        {**COMPANY_DATA, "name": "Company B"},
    )
    role_b = _create_role("Role B", company_b_id)
    p_id = _get_permission_id("DELETE_USER")
    _assign(role_b.id, p_id, company_b_id)

    with pytest.raises(RoleNotInCompany):
        role_permission_service.revoke_permission(role_b.id, p_id, company_a_id)


# --------------------------------------------------------
# role_has_permission
# --------------------------------------------------------

def test_role_has_permission_true():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    role = _create_role("Manager", company_id)
    p_id = _get_permission_id("READ_PRODUCT")
    _assign(role.id, p_id, company_id)

    assert role_permission_service.role_has_permission(role.id, p_id) is not None


def test_role_has_permission_false():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    role = _create_role("Manager", company_id)
    p_id = _get_permission_id("READ_PRODUCT")

    assert role_permission_service.role_has_permission(role.id, p_id) is None
