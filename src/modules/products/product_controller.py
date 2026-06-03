from flask import request, make_response, Blueprint
from flask_jwt_extended import jwt_required
from spectree import Response

from core.extensions import spectree
from .product_service import ProductService
from .product_repository import ProductRepository
from .product_model import (
    CreateProductInputModel,
    CreateProductOutputModel,
    UpdateProductInputModel,
    UpdateProductOutputModel,
    DetailProductModel,
    DeleteProductModel,
    ListDetailProductModel,
    ErrorOutput
)

from ..stock.stock_repository import StockRepository
from .product_middleware import require_user_from_same_company
from ..role_permissions.role_permission_middleware import require_permission
from .products_exceptions import ProductNotFound, ProductHasAlreadyStatus
from ..users_companies.auth_helpers import get_current_user_company

stock_repository = StockRepository()
product_repository = ProductRepository()

product_service = ProductService(product_repository, stock_repository)
product_controller = Blueprint(
    "product_controller",
    __name__,
    url_prefix="/products/api/v1"
)


# --------------------------------------------------------
# Error handlers
# --------------------------------------------------------

@product_controller.errorhandler(ProductNotFound)
def handle_not_found(error):
    return {"error": str(error)}, 404

@product_controller.errorhandler(ProductHasAlreadyStatus)
def handle_already_has_status(error):
    return {"error": str(error)}, 409

@product_controller.errorhandler(Exception)
def handle_generic_error(error):
    return {"error": "Internal server error", "detail": str(error)}, 500


# --------------------------------------------------------
# Endpoints
# --------------------------------------------------------

@product_controller.route("/create", methods=["POST"])
@jwt_required()
@require_permission("create_product")
@spectree.validate(
    json=CreateProductInputModel,
    resp=Response(
        HTTP_201=CreateProductOutputModel,
        HTTP_400=ErrorOutput
    ),
    tags=["Product"]
)
def create_product(json: CreateProductInputModel):
    data = json.model_dump()
    user_company = get_current_user_company()
    company_id = user_company.company_id

    product_service.create_product(data, company_id)
    return make_response({"msg": "Product created successfully"}, 201)


@product_controller.route("/get/<int:id>", methods=["GET"])
@jwt_required()
@require_user_from_same_company()
@require_permission("read_product")
@spectree.validate(
    resp=Response(
        HTTP_200=DetailProductModel,
        HTTP_400=ErrorOutput
    ),
    tags=["Product"]
)
def detail_product(id: int):
    if not id:
        return make_response({"error": "ID not provided"}, 400)

    product = product_service.get_product_by_id(id)
    return make_response({"product": product}, 200)


@product_controller.route("/update/<int:id>", methods=["PATCH", "PUT"])
@jwt_required()
@require_user_from_same_company()
@require_permission("update_product")
@spectree.validate(
    json=UpdateProductInputModel,
    resp=Response(
        HTTP_200=UpdateProductOutputModel,
        HTTP_400=ErrorOutput
    ),
    tags=["Product"]
)
def update_product(json: UpdateProductInputModel, id: int):
    if not id:
        return make_response({"error": "ID not provided"}, 400)

    data = json.model_dump(exclude_unset=True)
    product_service.update_product(id, data)
    return make_response({"msg": "Product updated successfully"}, 200)


@product_controller.route("/disable/<int:id>", methods=["DELETE"])
@jwt_required()
@require_user_from_same_company()
@require_permission("delete_product")
@spectree.validate(
    resp=Response(
        HTTP_200=DeleteProductModel,
        HTTP_400=ErrorOutput
    ),
    tags=["Product"]
)
def deactivate_product(id: int):
    if not id:
        return make_response({"error": "ID not provided"}, 400)

    data = {"status": "INACTIVE"}
    product_service.deactivate_product(id, data)
    return make_response({"msg": "Product deactivated successfully"}, 200)


@product_controller.route("/get/all", methods=["GET"])
@jwt_required()
@require_permission("read_product")
@spectree.validate(
    resp=Response(
        HTTP_200=ListDetailProductModel,
        HTTP_400=ErrorOutput
    )
)
def get_all_products():
    user_company = get_current_user_company()
    company_id = user_company.company_id

    page = max(int(request.args.get('page', 1)), 1)
    per_page = min(max(int(request.args.get('per_page', 10)), 1), 100)
    search = request.args.get('search')

    products, total = product_service.get_products(company_id, page, per_page, search)

    return make_response({
        "products": products,
        "total": total,
        "page": page,
        "per_page": per_page
    }, 200)


@product_controller.route("/search/<string:name>", methods=["GET"])
@jwt_required()
@require_permission("read_product")
@spectree.validate(
    resp=Response(
        HTTP_200=DetailProductModel,
        HTTP_400=ErrorOutput
    )
)
def get_product_by_name(name: str):
    user_company = get_current_user_company()
    company_id = user_company.company_id

    product = product_service.get_product_by_name(name, company_id)
    return make_response({'product': product}, 200)