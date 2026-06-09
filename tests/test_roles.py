import pytest

from modules.users.user_orchestrator import user_service
from modules.users_companies.users_companies_repository import UsersCompaniesRepository

from modules.roles.role_service import RoleService
from modules.roles.role_repository import RoleRepository
from modules.roles.role_entity import RoleEntity
from modules.roles.role_exceptions import (
    RoleNotFound,
    RoleIsAlreadyInactive,
    RoleNameReserved,
    UserNotInCompany,
)

users_companies_repo = UsersCompaniesRepository()
role_repo = RoleRepository()
role_service = RoleService(role_repo, users_companies_repo)

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

def _create_role_direct(name: str, company_id: int) -> RoleEntity:
    return role_repo.create_role(RoleEntity(name=name, company_id=company_id))

def _create_user_for_company(email: str, role_id: int, company_id: int) -> int:
    user_service.create_user_for_company(
        {
            "email": email,
            "first_name": "Worker",
            "last_name": "User",
            "password": "SecurePass123!",
            "role_id": role_id,
        },
        company_id,
    )
    from modules.users.user_repository import UserRepository
    return UserRepository().get_user_by_email(email).id


# --------------------------------------------------------
# Create
# --------------------------------------------------------

def test_create_role_success():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)

    role = role_service.create_role({"name": "Manager"}, company_id)

    assert role is not None
    assert role.name == "MANAGER"
    assert role.company_id == company_id


def test_create_role_reserved_name():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)

    with pytest.raises(RoleNameReserved):
        role_service.create_role({"name": "DEFAULT"}, company_id)


def test_create_role_reserved_name_case_insensitive():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)

    with pytest.raises(RoleNameReserved):
        role_service.create_role({"name": "default"}, company_id)


# --------------------------------------------------------
# Get
# --------------------------------------------------------

def test_get_role_by_id_success():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    role = _create_role_direct("Analyst", company_id)

    result = role_service.get_role_by_id(role.id)

    assert result["id"] == role.id


def test_get_role_by_id_not_found():
    with pytest.raises(RoleNotFound):
        role_service.get_role_by_id(99999)


def test_get_roles_from_company():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    _create_role_direct("Role A", company_id)
    _create_role_direct("Role B", company_id)

    result = role_service.get_roles_from_company(company_id, page=1, per_page=10)

    assert result.total >= 2


# --------------------------------------------------------
# Update
# --------------------------------------------------------

def test_update_role_success():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    role = _create_role_direct("Old Name", company_id)

    role_service.update_role(role.id, {"name": "New Name"})
    updated = role_service.get_role_by_id(role.id)

    assert updated["name"] == "NEW NAME"


def test_update_role_not_found():
    with pytest.raises(RoleNotFound):
        role_service.update_role(99999, {"name": "Whatever"})


# --------------------------------------------------------
# Delete (soft)
# --------------------------------------------------------

def test_delete_role_success():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    role = _create_role_direct("Temp Role", company_id)

    role_service.delete_soft_rol(role.id, {"status": "INACTIVE"})
    deleted = role_repo.get_role_by_id(role.id)

    assert deleted.status == "INACTIVE"


def test_delete_role_already_inactive():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    role = _create_role_direct("Once Role", company_id)
    role_service.delete_soft_rol(role.id, {"status": "INACTIVE"})

    with pytest.raises(RoleIsAlreadyInactive):
        role_service.delete_soft_rol(role.id, {"status": "INACTIVE"})


def test_delete_role_not_found():
    with pytest.raises(RoleNotFound):
        role_service.delete_soft_rol(99999, {"status": "INACTIVE"})


def test_delete_role_reassigns_users_to_default():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    role = _create_role_direct("Doomed Role", company_id)
    worker_id = _create_user_for_company("worker@test.com", role.id, company_id)

    role_service.delete_soft_rol(role.id, {"status": "INACTIVE"})

    membership = users_companies_repo.get_user_company_role_by_user_id(worker_id)
    reassigned_role = role_repo.get_role_by_id(membership.role_id)
    assert reassigned_role.name == "DEFAULT"


# --------------------------------------------------------
# Assign role
# --------------------------------------------------------

def test_assign_role_to_user_success():
    owner_id, company_id, owner_role_id = _register_owner(USER_DATA, COMPANY_DATA)
    new_role = _create_role_direct("New Role", company_id)
    worker_id = _create_user_for_company("assignee@test.com", owner_role_id, company_id)

    role_service.assign_role_to_user(worker_id, new_role.id, company_id)

    membership = users_companies_repo.get_user_company_role_by_user_id(worker_id)
    assert membership.role_id == new_role.id


def test_assign_role_user_not_in_company():
    _, company_a_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    _, company_b_id, _ = _register_owner(
        {**USER_DATA, "email": "owner_b@test.com"},
        {**COMPANY_DATA, "name": "Company B"},
    )
    role_b = _create_role_direct("Role B", company_b_id)
    worker_id = _create_user_for_company("worker_b@test.com", role_b.id, company_b_id)

    role_a = _create_role_direct("Role A", company_a_id)

    with pytest.raises(UserNotInCompany):
        role_service.assign_role_to_user(worker_id, role_a.id, company_a_id)


def test_assign_role_role_not_in_company():
    owner_id, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    _, other_company_id, _ = _register_owner(
        {**USER_DATA, "email": "owner2@test.com"},
        {**COMPANY_DATA, "name": "Other Corp"},
    )
    foreign_role = _create_role_direct("Foreign Role", other_company_id)

    with pytest.raises(RoleNotFound):
        role_service.assign_role_to_user(owner_id, foreign_role.id, company_id)
