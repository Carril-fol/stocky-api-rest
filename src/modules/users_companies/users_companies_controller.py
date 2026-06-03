from spectree import Response
from flask import Blueprint, make_response
from flask_jwt_extended import jwt_required

from core.extensions import spectree
from .auth_helpers import get_current_user_company
from .users_companies_model import RegisterInputFromCompany

from ..users.user_orchestrator import user_service
from ..users.user_middleware import require_user_from_same_company
from ..users.user_exceptions import UserNotFound, EmailInvalidFormat
from ..users.user_model import (
    RegisterOutput,
    UpdateUserInput,
    UpdateUserOutput,
    DeleteUserOutput,
    ErrorOutput
)

from ..permissions.permissions_exceptions import InsufficientRolePrivileges
from ..role_permissions.role_permission_middleware import require_permission

users_companies_blueprint = Blueprint(
    "users_companies", 
    __name__, 
    url_prefix="/users/api/v1"
)


# --------------------------------------------------------
# Error handlers
# --------------------------------------------------------

@users_companies_blueprint.errorhandler(UserNotFound)
def handle_not_found(error):
    return {'error': str(error)}, 404

@users_companies_blueprint.errorhandler(EmailInvalidFormat)
def handle_invalid_email(error):
    return {'error': str(error)}, 400

@users_companies_blueprint.errorhandler(InsufficientRolePrivileges)
def handle_insufficient_privileges(error):
    return {'error': str(error)}, 403

@users_companies_blueprint.errorhandler(Exception)
def handle_generic_error(error):
    return {'error': 'Internal server error', 'detail': str(error)}, 500


# --------------------------------------------------------
# Endpoints
# --------------------------------------------------------

@users_companies_blueprint.route("/create-user-from-company", methods=["POST"])
@jwt_required()
@require_permission("create_user")
@spectree.validate(
    json=RegisterInputFromCompany,
    resp=Response(
        HTTP_201=RegisterOutput,
        HTTP_400=ErrorOutput,
        HTTP_422=ErrorOutput,
        HTTP_403=ErrorOutput
    ),
    tags=["users"]
)
def create_user_for_company(json: RegisterInputFromCompany):
    data: dict = json.model_dump()
    company_id: int = get_current_user_company().company_id

    user_service.create_user_for_company(data, company_id)
    return make_response({"msg": "User created successfully"}, 201)


@users_companies_blueprint.route("/update-user-from-company/<int:id>", methods=["PUT", "PATCH"])
@jwt_required()
@require_user_from_same_company()
@require_permission("update_user")
@spectree.validate(
    json=UpdateUserInput,
    resp=Response(
        HTTP_200=UpdateUserOutput,
        HTTP_400=ErrorOutput,
        HTTP_422=ErrorOutput,
        HTTP_403=ErrorOutput
    ),
    tags=["users"]
)
def update_user_from_company(json: UpdateUserInput, id: int):
    data: dict = json.model_dump(exclude_unset=True)
    requesting_user_id: int = get_current_user_company().user_id

    user_service.update_user_from_company(id, data, requesting_user_id)
    return make_response({"msg": "User updated successfully"}, 200)


@users_companies_blueprint.route("/delete-user-from-company/<int:id>", methods=["DELETE"])
@jwt_required()
@require_user_from_same_company()
@require_permission("delete_user")
@spectree.validate(
    resp=Response(
        HTTP_200=DeleteUserOutput,
        HTTP_400=ErrorOutput,
        HTTP_422=ErrorOutput,
        HTTP_403=ErrorOutput
    ),
    tags=["users"]
)
def delete_user_from_company(id: int):
    requesting_user_id: int = get_current_user_company().user_id

    user_service.delete_user_from_company(id, requesting_user_id)
    return make_response({"msg": "User deleted successfully"}, 200)


@users_companies_blueprint.route("/get-users-from-company", methods=["GET"])
@jwt_required()
@require_permission("read_user")
@spectree.validate(
    resp=Response(
        HTTP_200=list[RegisterOutput],
        HTTP_403=ErrorOutput
    ),
    tags=["users"]
)
def get_users_from_company():
    company_id: int = get_current_user_company().company_id
    users = user_service.get_users_from_company(company_id)
    return make_response({"users": users}, 200)