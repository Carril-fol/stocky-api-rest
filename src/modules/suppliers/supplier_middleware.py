from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request

from .supplier_repository import SupplierRepository
from .supplier_service import SupplierService
from ..users_companies.auth_helpers import get_current_user_company

supplier_repository = SupplierRepository()
supplier_service = SupplierService(supplier_repository)

def require_user_from_same_company():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            supplier_id_url = kwargs.get("id")

            current_user_company = get_current_user_company()
            company_id_from_supplier = supplier_service.get_supplier_by_id(supplier_id_url)["company_id"]

            if current_user_company.company_id != company_id_from_supplier:
                return jsonify({"error": "Access denied to this company"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator