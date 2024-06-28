import json

from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token as createAccessToken
from flask_jwt_extended import create_refresh_token as createRefreshToken
from flask_jwt_extended import jwt_required as jwtRequired

from ..repositories.userRepository import UserRepository
from ..services.userService import UserService
from ..dao.userDao import UserDAO
from ..schemas.userSchema import UserLoginSchema, UserRegisterSchema

# Services

userDao = UserDAO()
userService = UserService(UserRepository(userDao))

# Blueprint

userBlueprint = Blueprint("users", __name__)

@userBlueprint.route("/users/register", methods=["POST"])
def registerUser():
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
    schema = UserRegisterSchema()

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON in request"}), 400

    errors = schema.validate(data)
    if errors:
        return jsonify({"error": errors}), 400
    
    newUser = userService.createUser(
        data["firstName"], 
        data["lastName"],
        data["email"], 
        data["password"]
    )
    getUserCreated = userService.getUserById(newUser)
    responseUserData = json.loads(getUserCreated.json())
    accessToken = createAccessToken(responseUserData)
    return jsonify({"msg": "User created", "user": responseUserData, "accessToken": accessToken}), 201


@userBlueprint.route("/users/login", methods=["POST"])
def loginUser():
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
    schema = UserLoginSchema()

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON in request"}), 400
    
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": errors}), 400
    
    email = data["email"]
    password = data["password"]

    isUserExists = userService.authenticationUser(email, password)
    if not isUserExists:
        return jsonify({"error": "User not found"}), 404
    
    responseUserData = json.loads(isUserExists.json())
    refreshToken = createRefreshToken(responseUserData)
    accessToken = createAccessToken(responseUserData)
    return jsonify(
        {
            "msg": "Login succefully","tokens": {
                "accessToken": accessToken, 
                "refreshToken": refreshToken
            }
        }
    )


@userBlueprint.route("/users/<userId>", methods=["GET"])
def detailUser(userId: str):
    if not userId:
        return jsonify({"error": "Not data in URL"}), 400
    
    isUserExists = userService.getUserById(userId)
    if not isUserExists:
        return jsonify({"error": "User not found"}), 404
    
    responseUserData = json.loads(isUserExists.json())
    return jsonify({"user": responseUserData}), 200