import pytest
from pydantic import ValidationError

from modules.permissions.permissions_service import PermissionService
from modules.permissions.permissions_repository import PermissionRepository
from modules.permissions.permissions_exceptions import PermissionNotFound, PermissionAlreadyExists

permission_repo = PermissionRepository()
permission_service = PermissionService(permission_repo)

# --------------------------------------------------------
# Data
# --------------------------------------------------------

PERMISSION_DATA = {
    "name": "Permission test"
}


# --------------------------------------------------------
# Create
# --------------------------------------------------------

def test_create_permissions_success():
    permission_created = permission_service.create_permission(PERMISSION_DATA)

    assert permission_created.name == "PERMISSION TEST"


def test_create_permissions_fail():
    with pytest.raises(ValidationError):
        permission_service.create_permission({"name": "Te"})


def test_create_permissions_already_exists():
    permission_service.create_permission(PERMISSION_DATA)

    with pytest.raises(PermissionAlreadyExists):
        permission_service.create_permission(PERMISSION_DATA)


# --------------------------------------------------------
# Get
# --------------------------------------------------------

def test_get_permission_by_name():
    permission_created = permission_service.create_permission(PERMISSION_DATA)
    permission = permission_service.get_permission_by_name(permission_created.name)

    assert permission["name"] == "PERMISSION TEST"


def test_not_found_permission():
    with pytest.raises(PermissionNotFound):
        permission_service.get_permission_by_name("Test permission not found")