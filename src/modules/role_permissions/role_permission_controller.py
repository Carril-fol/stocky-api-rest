from core.extensions import spectree

from spectree import Response
from flask import Blueprint, make_response
from flask_jwt_extended import jwt_required

from .role_permission_middleware import require_permission
from .role_permissions_repository import RolePermissionsRepository
from .role_permission_service import RolePermissionService
from .role_permission_exceptions import RoleNotInCompany, RolePermissionNotFound
from .role_permission_model import (
    AssignRolePermissionInput,
    AssignRolePermissionOutput,
    UpdateRolePermissionInput,
    UpdateRolePermissionOutput,
    DeleteRolePermissionInput,
    ListRolePermissionsOutput,
    RevokeRolePermissionOutput,
    ErrorOutput
)
from ..roles.role_repository import RoleRepository
from ..users_companies.auth_helpers import get_current_user_company

role_permission_repo = RolePermissionsRepository()
role_repo = RoleRepository()
role_permission_service = RolePermissionService(role_permission_repo, role_repo)

role_permission_controller = Blueprint(
    "role-permission",
    __name__,
    url_prefix="/role-permissions/api/v1"
)


# --------------------------------------------------------
# Error handlers
# --------------------------------------------------------

@role_permission_controller.errorhandler(RoleNotInCompany)
def handle_role_not_in_company(error):
    return {"error": str(error)}, 403

@role_permission_controller.errorhandler(RolePermissionNotFound)
def handle_role_permission_not_found(error):
    return {"error": str(error)}, 404

@role_permission_controller.errorhandler(Exception)
def handle_generic_error(error):
    return {"error": "Internal server error", "detail": str(error)}, 500


# --------------------------------------------------------
# Endpoints
# --------------------------------------------------------

@role_permission_controller.route("/assign-permission-to-role", methods=["POST"])
@jwt_required()
@require_permission("assign_role_permission")
@spectree.validate(
    json=AssignRolePermissionInput,
    resp=Response(
        HTTP_201=AssignRolePermissionOutput,
        HTTP_400=ErrorOutput,
        HTTP_422=ErrorOutput,
        HTTP_429=ErrorOutput,
    ),
    tags=["role-permissions"]
)
def assign_role_permission(json: AssignRolePermissionInput):
    data = json.model_dump()
    user_data = get_current_user_company()
    company_id = user_data.company_id

    role_permission_service.assign_role_permission_service(data, company_id)
    return make_response({"msg": "Role Permission assigned successfuly"}, 201)


@role_permission_controller.route("/update/<int:role_id>", methods=["PUT", "PATCH"])
@jwt_required()
@require_permission("update_role_permission")
@spectree.validate(
    json=UpdateRolePermissionInput,
    resp=Response(
        HTTP_200=UpdateRolePermissionOutput,
        HTTP_403=ErrorOutput,
        HTTP_404=ErrorOutput,
        HTTP_422=ErrorOutput,
    ),
    tags=["role-permissions"]
)
def update_role_permission(role_id: int, json: UpdateRolePermissionInput):
    data = json.model_dump(exclude_unset=True)
    user_data = get_current_user_company()
    company_id = user_data.company_id

    role_permission_service.update_role_permission_service(role_id, data, company_id)
    return make_response({"msg": "Role Permission updated successfully"}, 200)


@role_permission_controller.route("/get/<int:role_id>", methods=["GET"])
@jwt_required()
@require_permission("read_role_permission")
@spectree.validate(
    resp=Response(
        HTTP_200=ListRolePermissionsOutput,
        HTTP_403=ErrorOutput,
    ),
    tags=["role-permissions"]
)
def list_role_permissions(role_id: int):
    user_data = get_current_user_company()
    company_id = user_data.company_id
    
    permissions = role_permission_service.list_permissions_by_role_id(role_id, company_id)
    return make_response({"role_id": role_id, "permissions": permissions}, 200)


@role_permission_controller.route("/revoke", methods=["DELETE"])
@jwt_required()
@require_permission("delete_role_permission")
@spectree.validate(
    json=DeleteRolePermissionInput,
    resp=Response(
        HTTP_200=RevokeRolePermissionOutput,
        HTTP_403=ErrorOutput,
        HTTP_404=ErrorOutput,
        HTTP_422=ErrorOutput,
    ),
    tags=["role-permissions"]
)
def revoke_role_permission(json: DeleteRolePermissionInput):
    data = json.model_dump()
    user_data = get_current_user_company()
    company_id = user_data.company_id

    role_permission_service.revoke_permission(data["role_id"], data["permission_id"], company_id)
    return make_response({"msg": "Permission revoked successfully"}, 200)

