import math
from flask import Blueprint, request, make_response
from flask_jwt_extended import jwt_required
from spectree import Response
from core.extensions import spectree

from .stock_middleware import require_user_from_same_company
from .stock_repository import StockRepository
from .stock_service import StockService
from .stock_exceptions import StockNotFound
from .stock_model import (
    UpdateStockInput,
    UpdateStockOutput,
    StockListDetail,
    StockItemResponse,
    ErrorOutput
)

from ..products.product_repository import ProductRepository
from ..role_permissions.role_permission_middleware import require_permission
from ..users_companies.auth_helpers import get_current_user_company

product_repository = ProductRepository()
stock_repository = StockRepository()
stock_service = StockService(stock_repository, product_repository)

stock_blueprint = Blueprint(
    'stock_controller', 
    __name__, 
    url_prefix='/stock/api/v1'
)


# --------------------------------------------------------
# Error handlers
# --------------------------------------------------------

@stock_blueprint.errorhandler(StockNotFound)
def handle_not_found(error):
    return {"error": str(error)}, 404

@stock_blueprint.errorhandler(Exception)
def handle_generic_error(error):
    return {"error": "Internal server error", "detail": str(error)}, 500


# --------------------------------------------------------
# Endpoints
# --------------------------------------------------------

@stock_blueprint.route('/get/all', methods=['GET'])
@jwt_required()
@require_permission("read_stock")
@spectree.validate(
    resp=Response(
        HTTP_200=StockListDetail,
        HTTP_400=ErrorOutput,
        HTTP_404=ErrorOutput,
        HTTP_500=ErrorOutput,
    ),
    tags=["stock"]
)
def get_all_stock():
    user_data = get_current_user_company()
    company_id = user_data.company_id

    page: int = max(request.args.get('page', 1, type=int), 1)
    per_page: int = min(max(request.args.get('per_page', 10, type=int), 1), 100)

    stock_data, total = stock_service.get_stock_detailed_with_product(page, per_page, company_id)
    return make_response({
        "data": stock_data,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": math.ceil(total / per_page) if total else 0
    }, 200)


@stock_blueprint.route('/get/<int:id>', methods=['GET'])
@jwt_required()
@require_user_from_same_company()
@require_permission("read_stock")
@spectree.validate(
    resp=Response(
        HTTP_200=StockItemResponse,
        HTTP_404=ErrorOutput,
        HTTP_500=ErrorOutput,
    ),
    tags=["stock"]
)
def get_stock_by_id(id: int):
    stock = stock_service.get_stock_by_id(id)
    return make_response({'data': stock}, 200)


@stock_blueprint.route('/update/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@require_user_from_same_company()
@require_permission("update_stock")
@spectree.validate(
    json=UpdateStockInput,
    resp=Response(
        HTTP_200=UpdateStockOutput,
        HTTP_400=ErrorOutput,
        HTTP_404=ErrorOutput,
        HTTP_500=ErrorOutput,
    ),
    tags=["stock"]
)
def update_stock(id: int, json: UpdateStockInput):
    data = json.model_dump(exclude_unset=True)

    stock_service.update_stock(id, data)
    return make_response({'msg': 'Stock updated successfully'}, 200)


@stock_blueprint.route('/get/low', methods=['GET'])
@jwt_required()
@require_permission("read_stock")
@spectree.validate(
    resp=Response(
        HTTP_200=StockListDetail,
        HTTP_400=ErrorOutput,
        HTTP_404=ErrorOutput,
        HTTP_500=ErrorOutput,
    ),
    tags=["stock"]
)
def get_low_stock():
    user_data = get_current_user_company()
    company_id = user_data.company_id
    
    page: int = max(request.args.get('page', 1, type=int), 1)
    per_page: int = min(max(request.args.get('per_page', 10, type=int), 1), 100)

    data, total = stock_service.get_stock_low(page, per_page, company_id)
    return make_response({
        'data': data,
        'total': total,
        'page': page,
        'per_page': per_page,
        'total_pages': math.ceil(total / per_page) if total else 0
    }, 200)