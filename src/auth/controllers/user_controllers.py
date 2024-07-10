import json
from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt

from auth.service.user_service import UserService
from auth.service.token_service import TokenService
from auth.decorators.decorators import token_not_in_blacklist

# Services
user_service = UserService()
token_service = TokenService()


class UserRegisterResource(Resource):
    """
    Example:

    POST: /users/register

    ```
    Application data:
    {
        "first_name": "First name from the user",
        "last_name": "Last name from the user",
        "email": "Email from the user",
        "password": "Password from the user",
        "confirm_password": "Confirmation from the password"
    }

    Successful response (code 201 - Created):
    {   
        "msg": "User created",
        "user": {
            "id": "Id from the user",
            "first_name": "First name from the user",
            "last_name": "Last name from the user",
            "email": "Email from the user",
            "password": "Password from the user",
            "confirm_password": "Confirmation from the password"
        },
        "access_token": "8uP9dv0czfTLY8WEma1fZyBYLzUedsXiwp31A4wQ6klpJclPYQyZDsFruLuybCd9..."
    }

    Response with validation errors (code 400 - Bad Request):
    {
        "email": ["This field has to be unique"],
        "password": ["Password must contain at least one number."],
        // Other errors of validation from the schema.
    }
    ```
    """
    
    def post(self):
        data = request.get_json()
        if not data:
            return {"error": "Missing JSON in request"}, 400       
        try:
            new_user = user_service.create_user(
                data["first_name"],
                data["last_name"],
                data["email"],
                data["password"],
                data["confirm_password"]
            )
            get_user_created = user_service.get_user_by_id(new_user)
            response_user_data = json.loads(get_user_created)
            access_token = create_access_token(response_user_data)
            return {"msg": "User created", "user": response_user_data, "access_token": access_token}, 201
        except Exception as error:
            return {"error": (str(error))}, 400


class UserLoginResource(Resource):
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
        "access_token": "8uP9dv0czfTLY8WEma1fZyBYLzUed.sXiwp31A4wQ6klpJclPYQyZDsFruLuybCsd..."
        "refresh_token": "8uP9dv0czfTLY8WEma1fZyBYLzUed.sXiwp31A4wQ6klpJclPYQyZDsFruLuybCd9..."
    }

    Response with errors (code 400 - BAD REQUEST):
    {
        "email": "This field has to be unique.",
        // Other errors of validation from the schema.
    }
    ```
    """
    
    def post(self):
        data = request.get_json()
        if not data:
            return {"error": "Missing JSON in request"}, 400
        email = data["email"]
        password = data["password"]
        try:
            user_exists = user_service.authenticate_user(email, password)
            response_user_data = json.loads(user_exists)
            refresh_token = create_refresh_token(response_user_data)
            access_token = create_access_token(response_user_data)
            return {"msg": "Login succefully", "tokens": { "access_token": access_token, "refresh_token": refresh_token}}, 200
        except Exception as error:
            return {"error": (str(error))}, 400


class UserDetailsResource(Resource):
    """
    Example:

    GET: /users/<user_id>
    ```
    Header Authorization:
    {
        Authorization: "8uP9dv0czfTLY8WEma1fZyBYLzUedsX.iwp31A4wQ6klpJclPYQyZDsFruLuybCd9..."
    }

    Successful response (code 200 - OK):
    {
        "user": {
            "id": "Id from the user",
            "first_name": "First name from the user",
            "last_name": "Last name from the user",
            "email": "Email from the user",
            "password": "Password from the user"
        }
    }

    Response with errors (code 401 - UNAUTHORIZED):
    {
        "msg": "Missing Authorization Header"
    }
    ```
    """
    
    @jwt_required(locations=["headers"], optional=False)
    @token_not_in_blacklist
    def get(self, user_id: str):
        if not user_id:
            return {"error": "Not data in URL"}, 400
        try:
            user_exists = user_service.get_user_by_id(user_id)
            response_user_data = json.loads(user_exists)
            return {"user": response_user_data}, 200
        except Exception as error:
            return {"error": (str(error))}, 400
        

class UserLogoutResource(Resource):
    """
    Example:

    GET: /users/logout
    ```
    Header Authorization:
    {
        Authorization: "8uP9dv0czfTLY8WEma1fZyBYLzUedsX.iwp31A4wQ6klpJclPYQyZDsFruLuybCd9..."
    }

    Successful response (code 200 - OK):
    {
        "msg": "Logout succesfully"
    }

    Response with errors (code 400 - BAD REQUEST):
    {
        "msg": "Missing Authorization Header"
    }
    ```
    """

    @jwt_required(locations=["headers"], optional=False)
    def post(self):
        try:
            token_jti = get_jwt().get("jti")
            blacklist_token = token_service.blacklist_token(token_jti)
            return {"msg": "Logout succesfully"}, 200
        except Exception as error:
            return {"error": str(error)}, 400
