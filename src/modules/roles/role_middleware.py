from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request

from .role_repository import RoleRepository
from .role_service import RoleService
from ..users_companies.users_companies_repository import UsersCompaniesRepository
from ..users_companies.auth_helpers import get_current_user_company

users_companies_repository = UsersCompaniesRepository()
role_repository = RoleRepository()
role_service = RoleService(role_repository, users_companies_repository)

def require_user_from_same_company():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            role_id_url = kwargs.get("id")

            current_user_company = get_current_user_company()
            company_id_from_role = role_service.get_role_by_id(role_id_url)["company_id"]

            if current_user_company.company_id != company_id_from_role:
                return jsonify({"error": "Access denied to this company"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator

