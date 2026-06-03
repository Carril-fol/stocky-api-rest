from functools import wraps
from flask_jwt_extended import verify_jwt_in_request

from .role_permissions_repository import RolePermissionsRepository
from ..users_companies.auth_helpers import get_current_user_company

role_permissions_repo = RolePermissionsRepository()

def require_permission(permission: str):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            user_company = get_current_user_company()

            if user_company is None:
                return {"error": "Forbidden"}, 403

            permissions = role_permissions_repo.get_all_permissions_by_role_id(user_company.role_id)
            if permission not in permissions:
                return {"error": "Forbidden"}, 403

            return f(*args, **kwargs)
        return wrapper
    return decorator

