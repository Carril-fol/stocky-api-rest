import math
from flask import request, make_response, Blueprint
from flask_jwt_extended import jwt_required
from spectree import Response

from core.logger import get_logger
from core.extensions import spectree
from .category_repository import CategoryRepository
from .category_service import CategoryService
from .category_model import (
    CreateCategoryInput, 
    CreateCategoryOutput, 
    UpdateCategoryInput,
    UpdateCategoryOutput,
    DeleteCategoryOutput,
    DetailCategoryResponse,
    ListDetailCategoryModel,
    ErrorOutput
)
from ..products.product_repository import ProductRepository
from .categories_exceptions import CategoryNotFound, CategoryAlreadyExists, CategoryStatusError, CategoryNameReserved
from ..role_permissions.role_permission_middleware import require_permission
from ..users_companies.auth_helpers import get_current_user_company

logger = get_logger(__name__)

product_repository = ProductRepository()
category_repository = CategoryRepository()
category_service = CategoryService(category_repository, product_repository)

category_controller = Blueprint(
    'category_controller',
    __name__,
    url_prefix='/categories/api/v1'
)

# --------------------------------------------------------
# Error handlers
# --------------------------------------------------------

@category_controller.errorhandler(CategoryNotFound)
def handle_not_found(error):
    return {"error": str(error)}, 404

@category_controller.errorhandler(CategoryAlreadyExists)
def handle_already_exists(error):
    return {"error": str(error)}, 409

@category_controller.errorhandler(CategoryStatusError)
def handle_status_error(error):
    return {"error": str(error)}, 409

@category_controller.errorhandler(CategoryNameReserved)
def handle_name_reserved(error):
    return {"error": str(error)}, 409

@category_controller.errorhandler(Exception)
def handle_generic_error(error):
    return {"error": "Internal server error", "detail": str(error)}, 500


# --------------------------------------------------------
# Endpoints
# --------------------------------------------------------

@category_controller.route('/create', methods=['POST'])
@jwt_required()
@require_permission("create_category")
@spectree.validate(
    json=CreateCategoryInput,
    resp=Response(
        HTTP_201=CreateCategoryOutput, 
        HTTP_400=ErrorOutput
    ),
    tags=["Categories"]
)
def create_category(json: CreateCategoryInput):
    data = json.model_dump()
    user_company = get_current_user_company()
    company_id = user_company.company_id

    category_service.create_category(data, company_id)

    logger.info("Category created: name=%s company_id=%s", data.get("name"), company_id)
    return make_response({'msg': 'Category created successfully'}, 201)


@category_controller.route('/get/<int:id>', methods=['GET'])
@jwt_required()
@require_permission("read_category")
@spectree.validate(
    resp=Response(
        HTTP_200=DetailCategoryResponse,
        HTTP_404=ErrorOutput
    ),
    tags=["Categories"]
)
def get_category_by_id(id: int):
    user_company = get_current_user_company()
    company_id = user_company.company_id

    category = category_service.get_category_by_id(id, company_id)

    logger.info("Category retrieved: id=%s company_id=%s", id, company_id)
    return make_response({'category': category}, 200)


@category_controller.route('/get/all', methods=['GET'])
@jwt_required()
@require_permission("read_category")
@spectree.validate(
    resp=Response(
        HTTP_200=ListDetailCategoryModel,
        HTTP_400=ErrorOutput
    ),
    tags=["Categories"]
)
def get_all_categories_from_company():
    user_company = get_current_user_company()
    company_id = user_company.company_id

    page = max(request.args.get('page', 1, type=int), 1)
    per_page = min(max(request.args.get('per_page', 10, type=int), 1), 100)

    categories, total = category_service.get_all_categories_from_company(company_id, page, per_page)

    logger.info("Categories retrieved: company_id=%s page=%s per_page=%s", company_id, page, per_page)
    return make_response({
        "categories": categories,
        "total": total,
        "page": page,
        "per_page": per_page,
        "total_pages": math.ceil(total / per_page) if total else 0
    }, 200)


@category_controller.route('/update/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@require_permission("update_category")
@spectree.validate(
    json=UpdateCategoryInput,
    resp=Response(
        HTTP_200=UpdateCategoryOutput, 
        HTTP_400=ErrorOutput
    ),
    tags=["Categories"]
)
def update_category(json: UpdateCategoryInput, id: int):
    data = json.model_dump(exclude_unset=True)
    user_company = get_current_user_company()
    company_id = user_company.company_id

    category_service.update_category(id, data, company_id)

    logger.info("Category updated: id=%s fields=%s", id, list(data.keys()))
    return make_response({'msg': 'Category updated successfully'}, 200)


@category_controller.route('/disable/<int:id>', methods=['DELETE'])
@jwt_required()
@require_permission("delete_category")
@spectree.validate(
    resp=Response(
        HTTP_200=DeleteCategoryOutput, 
        HTTP_400=ErrorOutput
    ),
    tags=["Categories"]
)
def delete_category(id: int):
    data = {"status": "INACTIVE"}
    user_company = get_current_user_company()
    company_id = user_company.company_id

    category_service.delete_category(id, data, company_id)

    logger.info("Category deleted: id=%s company_id=%s", id, company_id)
    return make_response({'msg': 'Category deleted successfully'}, 200)


@category_controller.route('/search/<string:name>', methods=['GET'])
@jwt_required()
@require_permission("read_category")
@spectree.validate(
    resp=Response(
        HTTP_200=DetailCategoryResponse,
        HTTP_404=ErrorOutput
    ),
    tags=["Categories"]
)
def get_category_by_name(name: str):
    user_company = get_current_user_company()
    company_id = user_company.company_id

    category = category_service.get_category_by_name(name, company_id)

    logger.info("Category retrieved by name: name=%s company_id=%s", name, company_id)
    return make_response({'category': category}, 200)