from datetime import timedelta
from spectree import Response
from flask import Blueprint, make_response
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    unset_access_cookies,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies
)

from core.extensions import limiter, spectree
from .user_orchestrator import user_service
from .user_exceptions import UserNotFound, EmailInvalidFormat
from .user_model import (
    LoginInput,
    LoginOutput,
    RegisterWithCompanyInput,
    RegisterOutput,
    ErrorOutput
)

from ..users_companies.auth_helpers import get_current_user_company
from ..permissions.permissions_exceptions import InsufficientRolePrivileges
from ..role_permissions.role_permission_middleware import require_permission

users_blueprint = Blueprint(
    "users", 
    __name__, 
    url_prefix="/users/api/v1"
)

# --------------------------------------------------------
# Error handlers
# --------------------------------------------------------

@users_blueprint.errorhandler(UserNotFound)
def handle_not_found(error):
    return {'error': str(error)}, 404

@users_blueprint.errorhandler(EmailInvalidFormat)
def handle_invalid_email(error):
    return {'error': str(error)}, 400

@users_blueprint.errorhandler(InsufficientRolePrivileges)
def handle_insufficient_privileges(error):
    return {'error': str(error)}, 403

@users_blueprint.errorhandler(Exception)
def handle_generic_error(error):
    return {'error': 'Internal server error', 'detail': str(error)}, 500


# --------------------------------------------------------
# Endpoints from auth
# --------------------------------------------------------

@users_blueprint.route("/register", methods=["POST"])
@limiter.limit("3 per hour")
@spectree.validate(
    json=RegisterWithCompanyInput,
    resp=Response(
        HTTP_201=RegisterOutput,
        HTTP_400=ErrorOutput,
        HTTP_422=ErrorOutput,
        HTTP_429=ErrorOutput,
    ),
    tags=["auth"]
)
def register(json: RegisterWithCompanyInput):
    data = json.model_dump()
    identity = user_service.register_owner(data["user"], data["company"])
    access_token = create_access_token(identity=str(identity), expires_delta=timedelta(minutes=30))

    response = make_response({"msg": "Register successful", "access_token": access_token}, 201)
    set_access_cookies(response, access_token)
    return response


@users_blueprint.route("/login", methods=["POST"])
@limiter.limit("5 per minute")
@spectree.validate(
    json=LoginInput,
    resp=Response(
        HTTP_200=LoginOutput,
        HTTP_404=ErrorOutput,
        HTTP_422=ErrorOutput,
        HTTP_429=ErrorOutput
    ),
    tags=["auth"],
)
def login(json: LoginInput):
    data = json.model_dump()
    user_id = user_service.authenticate_user(data)

    access_token = create_access_token(str(user_id))
    refresh_token = create_refresh_token(str(user_id))

    response = make_response({"msg": "Login successful", "access_token": access_token}, 200)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response


@users_blueprint.route("/logout", methods=["POST"])
@jwt_required()
@spectree.validate(tags=["auth"])
def logout():
    response = make_response({"msg": "Logout succesfully"}, 200)
    unset_access_cookies(response)
    unset_jwt_cookies(response)
    return response


@users_blueprint.route("/refresh", methods=["POST"])
@jwt_required(verify_type=True, refresh=True)
@spectree.validate(tags=["auth"])
def refresh_token():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    new_refresh_token = create_refresh_token(identity=current_user)

    response = make_response({"msg": "Token refreshed", "tokens": {
        "access_token": new_access_token, 
        "refresh_token": new_refresh_token
        }
    }, 200)
    set_access_cookies(response, new_access_token)
    set_refresh_cookies(response, new_refresh_token)
    return response


@users_blueprint.route("/me", methods=["GET"])
@jwt_required()
@spectree.validate(tags=["auth"])
def me():
    user_id: int = get_current_user_company().user_id
    
    user_instance = user_service.get_user_by_id(user_id)
    return make_response({"user": user_instance}, 200)