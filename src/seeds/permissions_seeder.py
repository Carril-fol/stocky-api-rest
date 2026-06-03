import json
from pathlib import Path

from modules.permissions.permissions_repository import PermissionRepository
from modules.permissions.permissions_service import PermissionService
from modules.permissions.permissions_exceptions import PermissionNotFound

permission_repo = PermissionRepository()
permission_service = PermissionService(permission_repo)

def seed_permissions():
    path = Path(__file__).parent / "permissions.json"
    with open(path, "r") as f:
        data = json.load(f)
    
    for permission_name in data["permissions"]:
        try:
            permission_service.get_permission_by_name(permission_name)
        except PermissionNotFound:
            permission_service.create_permission({"name": permission_name})