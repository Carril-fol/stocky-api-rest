import json
from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token

from ..repositories.user_repository import UserRepository
from ..services.user_service import UserService
from ..dao.user_dao import UserDAO

# Dao
user_dao = UserDAO()

# Services
user_service = UserService(UserRepository(user_dao))

# Blueprint
user_blueprint = Blueprint("users", __name__)

@user_blueprint.route("/users/register", methods=["POST"])
def register_user():
    """
    Example:

    POST: /users/register

    ```
    Application data:
    {
        "firstName": "First name from the user",
        "lastName": "Last name from the user",
        "email": "Email from the user",
        "password": "Password from the user",
        "confirm_password": "Confirmation from the password"
    }

    Successful response (code 201 - Created):
    {   
        "msg": "User created",
        "user":     {
            "id": "Id from the user",
            "firstName": "First name from the user",
            "lastName": "Last name from the user",
            "email": "Email from the user",
            "password": "Password from the user",
            "confirmPassword": "Confirmation from the password"
        },
        "access_token": "8uP9dv0czfTLY8WEma1fZyBYLzUedsXiwp31A4wQ6klpJclPYQyZDsFruLuybCd9"
    }

    Response with validation errors (code 400 - Bad Request):
    {
        "email": ["This field has to be unique"],
        "password": ["Password must contain at least one number."],
        // Other errors of validation from the schema.
    }
    ```
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON in request"}), 400
    
    try:
        new_user = user_service.create_user(
            data["first_name"], 
            data["last_name"],
            data["email"], 
            data["password"],
            data["confirm_password"]
        )
        get_user_created = user_service.get_user_by_id(new_user)
        response_user_data = json.loads(get_user_created.json())
        access_token = create_access_token(response_user_data)
        return jsonify(
            {
                "msg": "User created",
                "user": response_user_data,
                "token": access_token
            }
        ), 201
    except Exception as error:
        return jsonify({"error": (str(error))}), 400


@user_blueprint.route("/users/login", methods=["POST"])
def login_user():
    """
    Example:

    POST: /users/login

    ```
    Application data:
    {
        "email": "Email from the user",
        "password": "Password from the user"
    }

    Successful response (code 200 - OK):
    {
        "message": "Login successful"
        "refresh_token": "8uP9dv0czfTLY8WEma1fZyBYLzUedsXiwp31A4wQ6klpJclPYQyZDsFruLuybCd9"
    }

    Response with validation errors (code 400 - BAD REQUEST):
    {
        "email": ["This field has to be unique."],
        // Other errors of validation from the schema.
    }
    ```
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON in request"}), 400   
    try:
        email = data["email"]
        password = data["password"]
        user_exists = user_service.authenticate_user(email, password)
        if not user_exists:
            return jsonify({"error": "User not found"}), 404 
        response_user_data = json.loads(user_exists.json())
        refresh_token = create_access_token(response_user_data)
        access_token = create_refresh_token(response_user_data)
        return jsonify(
            {
                "msg": "Login succefully", 
                "tokens": {
                    "access_token": access_token, 
                    "refresh_token": refresh_token
                }
            }
        )
    except Exception as error:
        return jsonify({"error": (str(error))}), 400


@user_blueprint.route("/users/<user_id>", methods=["GET"])
def detail_user(user_id: str):
    if not user_id:
        return jsonify({"error": "Not data in URL"}), 400
    try:
        is_user_exists = user_service.get_user_by_id(user_id)
        if not is_user_exists:
            return jsonify({"error": "User not found"}), 404    
        response_user_data = json.loads(is_user_exists.json())
        return jsonify({"user": response_user_data}), 200
    except Exception as error:
        return jsonify({"error": (str(error))}), 400