import json
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from ..services.category_service import CategoryService

category_service = CategoryService()

class CategoryCreateResource(Resource):
    """
    Example:

    POST: /categories/api/v1/create
    ```
    Application data:
    {
        "name": "Name for the category"
    }

    Successful response (code 201 - CREATED):
    {   
        "msg": "Category created",
        "category": {
            "id": "Id from category",
            "name": "Name from category"
        }
    }

    Response with validation errors (code 400 - BAD REQUEST):
    {
        "error": "Category already exists."
    }
    ```
    """
    @jwt_required(locations=["headers"])
    def post(self):
        data = request.get_json()
        if not data:
            return {"error": "Missing JSON in request"}, 400
        try:
            category_created = category_service.create_category(data["name"])
            get_category_created = category_service.get_category_by_id(category_created)
            response_category_data = json.loads(get_category_created)
            return {"status": "Created", "category": response_category_data}, 201
        except Exception as error:
            return {"error": str(error)}, 400


class CategoryDetailByNameResource(Resource):
    """
    Example:

    POST: /categories/api/v1/<name>
    ```
    URL data:
    {
        "name": "Name for the category"
    }

    Successful response (code 200 - OK):
    {   
        "category": {
            "id": "Id from category",
            "name": "Name from category"
        }
    }

    Response with validation errors (code 400 - BAD REQUEST):
    {
        "error": "Category not found."
    }
    ```
    """
    @jwt_required(locations=["headers"])
    def get(self, name: str):
        if not name:
            return {"error": "Missing JSON in request"}, 400
        try:
            category = category_service.get_category_by_name(name)
            response_category_data = json.loads(category)
            return {"category": response_category_data}, 200
        except Exception as error:
            return {"error": str(error)}, 400


class CategoryAllDetailResource(Resource):
    """
    Example:

    POST: /categories/api/v1/all
    ```
    Successful response (code 200 - OK):
    {   
        "categories": [
            {
                "id": "Id from category",
                "name": "Name from category"
            },
            ...
        ]
    }
    ```
    """
    @jwt_required(locations=["headers"])
    def get(self):
        categories = category_service.get_all_categories()
        return {"categories": categories}, 200


class CategoryDeleteResource(Resource):
    """
    Example:

    DELETE: /categories/api/v1/delete/<category_id>
    ```
    URL data:
    {
        "category_id": "Id from the category"
    }

    Successful response (code 200 - OK):
    {   
        "category": "Deleted"
    }
    ```
    """
    @jwt_required(locations=["headers"])
    def delete(self, category_id: str):
        if not category_id:
            return {"error": "Missing JSON in request"}, 400
        try:
            category_delete = category_service.delete_category(category_id)
            return {"status": "Deleted"}, 200
        except Exception as error:
            return {"error": str(error)}, 400


class CategoryUpdateResource(Resource):
    """
    Example:

    PUT: /categories/api/v1/update/<category_id>
    ```
    URL data:
    {
        "category_id": "Id from the category"
    }

    Application data:
    {
        "name": "New name for the category"
    }

    Successful response (code 200 - OK):
    {   
        "staus": "Update",
        "category": {
            "id": "Id from category",
            "name": "New name from category"
        }
    }
    ```
    """
    @jwt_required(locations=["headers"])
    def put(self, category_id: str):
        data = request.get_json()
        if not category_id:
            return {"error": "Missing JSON in request"}, 400
        try:
            category_update = category_service.update_category(category_id, data["name"])
            get_category_updated = category_service.get_category_by_id(category_update)
            response_category_data = json.loads(get_category_updated)
            return {"status": "Update", "category": response_category_data}, 200
        except Exception as error:
            return {"error": str(error)}, 400

