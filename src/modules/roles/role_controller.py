from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from spectree import Response

from core.extensions import spectree
from core.logger import get_logger
from .role_middleware import require_user_from_same_company
from .role_service import RoleService
from .role_repository import RoleRepository
from .role_exceptions import RoleNotFound, RoleIsAlreadyInactive, UserNotInCompany, RoleNameReserved
from .role_model import (
    CreateRoleInput,
    CreateRoleOutput,
    UpdateRoleInput,
    UpdateRoleOutput,
    AssignRoleInput,
    AssignRoleOutput,
    DetailRoleModel,
    RoleListDetail,
    DeleteRoleOutput,
    ErrorOutput
)

from ..users_companies.auth_helpers import get_current_user_company
from ..role_permissions.role_permission_middleware import require_permission
from ..users_companies.users_companies_repository import UsersCompaniesRepository
 
logger = get_logger(__name__)

users_companies_repository = UsersCompaniesRepository()
role_repository = RoleRepository()
role_service = RoleService(role_repository, users_companies_repository)
role_blueprint = Blueprint("roles", __name__, url_prefix="/roles/api/v1")
 

# --------------------------------------------------------
# Error handlers
# --------------------------------------------------------

@role_blueprint.errorhandler(RoleNotFound)
def handle_not_found(error):
    return {"error": str(error)}, 404
 
@role_blueprint.errorhandler(RoleIsAlreadyInactive)
def handle_already_inactive(error):
    return {"error": str(error)}, 409
 
@role_blueprint.errorhandler(UserNotInCompany)
def handle_user_not_in_company(error):
    return {"error": str(error)}, 403

@role_blueprint.errorhandler(RoleNameReserved)
def handle_name_reserved(error):
    return {"error": str(error)}, 409
 
@role_blueprint.errorhandler(Exception)
def handle_generic_error(error):
    logger.exception(error)
    return {"error": "Internal server error"}, 500


# --------------------------------------------------------
# Endpoints
# --------------------------------------------------------

@role_blueprint.route("/create-role", methods=["POST"])
@jwt_required()
@require_permission("create_role")
@spectree.validate(
    json=CreateRoleInput,
    resp=Response(
        HTTP_201=CreateRoleOutput,
        HTTP_403=ErrorOutput,
        HTTP_404=ErrorOutput,
        HTTP_422=ErrorOutput
    ),
    tags=["roles"]
)
def create_role(json: CreateRoleInput):
    data = json.model_dump()
    company_id = get_current_user_company().company_id

    role_service.create_role(data, company_id)
    logger.info("Role created: company_id=%s", company_id)
    return {"msg": "Role created successfully"}, 201

@role_blueprint.route("/get-roles", methods=["GET"])
@jwt_required()
@require_permission("read_role")
@spectree.validate(
    resp=Response(
        HTTP_200=RoleListDetail,
        HTTP_403=ErrorOutput,
        HTTP_404=ErrorOutput,
        HTTP_422=ErrorOutput
    ),
    tags=["roles"]
)
def get_all_roles():
    page = max(request.args.get("page", 1, type=int), 1)
    per_page = min(max(request.args.get("per_page", 10, type=int), 1), 100)
    company_id = get_current_user_company().company_id
 
    result = role_service.get_roles_from_company(company_id, page, per_page)
    logger.info("Roles retrieved: company_id=%s", company_id)
    return result, 200


@role_blueprint.route("/get/<int:id>", methods=["GET"])
@jwt_required()
@require_permission("read_role")
@require_user_from_same_company()
@spectree.validate(
    resp=Response(
        HTTP_200=DetailRoleModel,
        HTTP_403=ErrorOutput,
        HTTP_404=ErrorOutput,
        HTTP_422=ErrorOutput
    ),
    tags=["roles"]
)
def get_role_by_id(id: int):
    role = role_service.get_role_by_id(id)
    logger.info("Role retrieved: id=%s", id)
    return role, 200


@role_blueprint.route("/delete/<int:id>", methods=["DELETE"])
@jwt_required()
@require_permission("delete_role")
@require_user_from_same_company()
@spectree.validate(
    resp=Response(
        HTTP_200=DeleteRoleOutput,
        HTTP_403=ErrorOutput,
        HTTP_404=ErrorOutput,
        HTTP_422=ErrorOutput
    ),
    tags=["roles"]
)
def delete_role(id: int):
    role_service.delete_soft_rol(id, {"status": "INACTIVE"})
    logger.info("Role deleted: id=%s", id)
    return {"msg": "Role deleted successfully"}, 200


@role_blueprint.route("/update/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
@require_permission("update_role")
@require_user_from_same_company()
@spectree.validate(
    json=UpdateRoleInput,
    resp=Response(
        HTTP_200=UpdateRoleOutput,
        HTTP_403=ErrorOutput,
        HTTP_404=ErrorOutput,
        HTTP_422=ErrorOutput,
    ),
    tags=["roles"]
)
def update_role(id: int, json: UpdateRoleInput):
    role_service.update_role(id, json.model_dump(exclude_unset=True))
    logger.info("Role updated: id=%s", id)
    return {"msg": "Role updated successfully"}, 200


@role_blueprint.route("/assign-role", methods=["PATCH"])
@jwt_required()
@require_permission("assign_role")
@spectree.validate(
    json=AssignRoleInput,
    resp=Response(
        HTTP_200=AssignRoleOutput,
        HTTP_403=ErrorOutput,
        HTTP_404=ErrorOutput,
        HTTP_422=ErrorOutput,
    ),
    tags=["roles"]
)
def assign_role_to_user(json: AssignRoleInput):
    data = json.model_dump()
    company_id = get_current_user_company().company_id

    role_service.assign_role_to_user(data["user_id"], data["role_id"], company_id)
    logger.info("Role assigned: user_id=%s role_id=%s", data["user_id"], data["role_id"])
    return {"msg": "Role reassigned successfully"}, 200