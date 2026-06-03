from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request

from .stock_repository import StockRepository
from .stock_service import StockService
from ..products.product_repository import ProductRepository
from ..users_companies.auth_helpers import get_current_user_company

product_repository = ProductRepository()
stock_repository = StockRepository()
stock_service = StockService(stock_repository, product_repository)

def require_user_from_same_company():
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            stock_id_url = kwargs.get("id")
            if not stock_id_url:
                return jsonify({"error": "Stock ID not provided"}), 400

            current_user_company = get_current_user_company()
            company_id_from_stock = stock_service.get_stock_by_id(stock_id_url)["product"]["company_id"]

            if current_user_company.company_id != company_id_from_stock:
                return jsonify({"error": "Access denied to this company"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator

