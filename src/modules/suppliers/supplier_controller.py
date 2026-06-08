from flask import Blueprint, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from spectree import Response
from core.extensions import spectree

from .supplier_middleware import require_user_from_same_company
from ..role_permissions.role_permission_middleware import require_permission
from .supplier_repository import SupplierRepository
from .supplier_service import SupplierService
from .supplier_exceptions import SupplierAlreadyExists, SupplierHasAlreadyStatus, SupplierNotFound
from .supplier_model import (
    CreateSupplierInput, 
    SupplierCreatedOutput,
    UpdateSupplierInput,
    SupplierUpdatedOutput,    
    SupplierDeletedOutput,
    SupplierDetailOutput, 
    SupplierListOutput, 
    ErrorOutput
)

from core.logger import get_logger

logger = get_logger(__name__)

supplier_controller = Blueprint('supplier_controller', __name__, url_prefix='/suppliers/api/v1')
supplier_repository = SupplierRepository()
supplier_service = SupplierService(supplier_repository)

# --------------------------------------------------------
# Error handlers
# --------------------------------------------------------

@supplier_controller.errorhandler(SupplierNotFound)
def handle_not_found(error):
    return {'error': str(error)}, 404

@supplier_controller.errorhandler(SupplierAlreadyExists)
def handle_already_exists(error):
    return {'error': str(error)}, 409

@supplier_controller.errorhandler(SupplierHasAlreadyStatus)
def handle_already_status(error):
    return {'error': str(error)}, 409

@supplier_controller.errorhandler(Exception)
def handle_generic_error(error):
    return {'error': 'Internal server error', 'detail': str(error)}, 500


# --------------------------------------------------------
# Endpoints
# --------------------------------------------------------

@supplier_controller.route('/create', methods=['POST'])
@jwt_required()
@require_user_from_same_company()
@require_permission("create_supplier")
@spectree.validate(
    json=CreateSupplierInput,
    resp=Response(
        HTTP_201=SupplierCreatedOutput,
        HTTP_409=ErrorOutput,
        HTTP_422=ErrorOutput
    ),
    tags=["suppliers"],
)
def create_supplier(json: CreateSupplierInput):
    data: dict = json.model_dump()
    user_data: dict = get_jwt_identity()
    company_id: int = user_data.get("user_role")["company_id"]

    supplier_service.create_supplier(data, company_id)
    logger.info("Supplier created: company_id=%s", company_id)
    return make_response({'msg': 'Supplier created successfully'}, 201)


@supplier_controller.route('/get/<int:id>', methods=['GET'])
@jwt_required()
@require_user_from_same_company()
@require_permission("read_supplier")
@spectree.validate(
    resp=Response(
        HTTP_200=SupplierDetailOutput,
        HTTP_409=ErrorOutput,
        HTTP_422=ErrorOutput
    ),
    tags=["suppliers"]
)
def get_supplier_by_id(id: int):
    supplier = supplier_service.get_supplier_by_id(id)
    logger.info("Supplier retrieved: id=%s", id)
    return make_response({'supplier': supplier}, 200)


@supplier_controller.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required()
@require_user_from_same_company()
@require_permission("delete_supplier")
@spectree.validate(
    resp=Response(HTTP_200=SupplierDeletedOutput),
    tags=["suppliers"],
)
def delete_supplier(id: int):
    data = {'status': 'INACTIVE'}
    supplier_service.delete_supplier(id, data)
    logger.info("Supplier deleted: id=%s", id)
    return make_response({'msg': 'Supplier deleted successfully'}, 200)


@supplier_controller.route('/', methods=['GET'])
@jwt_required()
@require_permission("read_supplier")
@spectree.validate(
    resp=Response(HTTP_200=SupplierListOutput),
    tags=["suppliers"],
)
def get_suppliers():
    user_data: dict = get_jwt_identity()
    company_id: int = user_data.get("user_role")["company_id"]

    suppliers = supplier_service.get_suppliers(company_id)
    logger.info("Suppliers retrieved: company_id=%s", company_id)
    return make_response({'suppliers': suppliers}, 200)


@supplier_controller.route('/update/<int:id>', methods=['PUT', 'PATCH'])
@jwt_required()
@require_user_from_same_company()
@require_permission("update_supplier")
@spectree.validate(
    json=UpdateSupplierInput,
    resp=Response(
        HTTP_200=SupplierUpdatedOutput,
        HTTP_409=ErrorOutput,
        HTTP_422=ErrorOutput
    ),
    tags=["suppliers"],
)
def update_supplier(json: UpdateSupplierInput, id: int):
    data = json.model_dump()

    user_data: dict = get_jwt_identity()
    company_id: int = user_data.get("user_role")["company_id"]

    supplier_service.update_supplier(id, data, company_id)
    logger.info("Supplier updated: id=%s", id)
    return make_response({'msg': 'Supplier updated successfully'}, 200)