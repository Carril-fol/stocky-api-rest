import pytest


from modules.users.user_orchestrator import user_service
from modules.users.user_repository import UserRepository
from modules.users.user_exceptions import UserWithAnEmailAlreadyExists, UserNotFound

from modules.role_permissions.role_permissions_repository import RolePermissionsRepository
from modules.role_permissions.role_permissions_entity import RolePermissionEntity

from modules.roles.role_entity import RoleEntity
from modules.roles.role_repository import RoleRepository

from modules.permissions.permissions_repository import PermissionRepository
from modules.permissions.permissions_entity import PermissionsEntity

from modules.users_companies.users_companies_repository import UsersCompaniesRepository
from modules.permissions.permissions_exceptions import InsufficientRolePrivileges


user_repo = UserRepository()
users_companies_repo = UsersCompaniesRepository()
role_permissions_repo = RolePermissionsRepository()
role_repo = RoleRepository()
permissions_repo = PermissionRepository()

# --------------------------------------------------------
# Helpers
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

def _register_owner(user_data: dict, company_data: dict):
    user_id = user_service.register_owner(user_data, company_data)
    users_companies_data = users_companies_repo.get_user_company_role_by_user_id(user_id)
    return user_id, users_companies_data.company_id, users_companies_data.role_id

def _create_role(company_id: int, name: str):
    role_repo = RoleRepository()
    role_entity = RoleEntity(
        name=name,
        company_id=company_id
    )
    return role_repo.create_role(role_entity)

def _create_user_for_company(user_data: dict, role_id: int, company_id: int):
    user_data["role_id"] = role_id
    user_service.create_user_for_company(user_data, company_id)
    return user_repo.get_user_by_email(user_data["email"]).id

def _assings_permission_to_role(role_id: int, permission_id: int):
    return role_permissions_repo.create_role_permission(
        role_permission_entity=RolePermissionEntity(
            role_id=role_id,
            permission_id=permission_id
        )
    )

# --------------------------------------------------------
# Register
# --------------------------------------------------------

def test_register_owner_success():
    user_id = user_service.register_owner(USER_DATA, COMPANY_DATA)
    assert isinstance(user_id, int)
    user = user_service.get_user_by_id(user_id)
    assert user["first_name"] == USER_DATA["first_name"].upper()
    assert user["last_name"] == USER_DATA["last_name"].upper()


def test_register_owner_duplicate_email():
    user_service.register_owner(USER_DATA, COMPANY_DATA)
    with pytest.raises(UserWithAnEmailAlreadyExists):
        user_service.register_owner(USER_DATA, COMPANY_DATA)


# --------------------------------------------------------
# Login
# --------------------------------------------------------

def test_login_success():
    user_service.register_owner(USER_DATA, COMPANY_DATA)
    user_id = user_service.authenticate_user({
        "email": USER_DATA["email"],
        "password": USER_DATA["password"],
    })
    assert isinstance(user_id, int)


def test_login_wrong_password():
    user_service.register_owner(USER_DATA, COMPANY_DATA)
    with pytest.raises(Exception):
        user_service.authenticate_user({
            "email": USER_DATA["email"],
            "password": "wrong-password",
        })


def test_login_email_not_found():
    with pytest.raises(UserNotFound):
        user_service.authenticate_user({
            "email": "notexists@test.com",
            "password": USER_DATA["password"],
        })


# --------------------------------------------------------
# Get / Delete
# --------------------------------------------------------

def test_get_user_not_found():
    with pytest.raises(UserNotFound):
        user_service.get_user_by_id(99999)


def test_delete_user_success():
    user_id = user_service.register_owner(USER_DATA, COMPANY_DATA)
    user_service.delete_user(user_id)
    with pytest.raises(UserNotFound):
        user_service.get_user_by_id(user_id)


# --------------------------------------------------------
# Management of users from company
# --------------------------------------------------------

def test_create_user_for_company_success():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    admin_role = _create_role(company_id, "ADMIN")

    user_id = _create_user_for_company({
        "email": "employee@test.com",
        "first_name": "Employee",
        "last_name": "User",
        "password": "securePassword123-"
    }, admin_role.id, company_id)

    user_created = users_companies_repo.get_user_company_role_by_user_id(user_id)
    assert user_created.company_id == company_id
    assert user_created.role_id == admin_role.id



def test_cannot_update_user_with_same_role():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    admin_role = _create_role(company_id, name="ADMIN")

    user2_id = _create_user_for_company(
        {"email": "admin1@test.com", "first_name": "Admin", "last_name": "One", "password": "SecurePass123!"},
        admin_role.id, company_id
    )
    user3_id = _create_user_for_company(
        {"email": "admin2@test.com", "first_name": "Admin", "last_name": "Two", "password": "SecurePass123!"},
        admin_role.id, company_id
    )

    with pytest.raises(InsufficientRolePrivileges):
        user_service.update_user_from_company(user3_id, {"first_name": "Changed"}, user2_id)


def test_cannot_delete_owner_user():
    owner_id, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    admin_role = _create_role(company_id, name="ADMIN")
    admin_id = _create_user_for_company(
        {"email": "admin@test.com", "first_name": "Admin", "last_name": "User", "password": "SecurePass123!"},
        admin_role.id, company_id
    )

    with pytest.raises(InsufficientRolePrivileges):
        user_service.delete_user_from_company(owner_id, admin_id)


# --------------------------------------------------------
# List users
# --------------------------------------------------------

def test_list_users_from_company():
    _, company_id, _ = _register_owner(USER_DATA, COMPANY_DATA)
    admin_role = _create_role(company_id, name="ADMIN")

    _create_user_for_company(
        {
            "email": "userexampleemail@gmail.com",
            "first_name": "User",
            "last_name": "Example",
            "password": "SecurePass123!"
        },
        admin_role.id, company_id
    )

    users = user_service.get_users_from_company(company_id)
    emails = [u["email"] for u in users]

    assert len(users) == 2
    assert "owner_b@test.com" not in emails
