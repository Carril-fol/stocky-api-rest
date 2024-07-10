import json
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from ..services.category_service import CategoryService

category_service = CategoryService()

class CategoryCreateResource(Resource):
    
    @jwt_required(locations=["headers"])
    def post(self):
        data = request.get_json()
        if not data:
            return {"error": "Missing JSON in request"}, 400
        try:
            category_created = category_service.create_category(data["name"])
            get_category_created = category_service.get_category_by_id(category_created)
            response_category_data = json.loads(get_category_created)
            return {"msg": "Category created", "category": response_category_data}, 201
        except Exception as error:
            return {"msg": str(error)}, 400


class CategoryDetailByNameResource(Resource):

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

    @jwt_required(locations=["headers"])
    def get_categories():
        categories = category_service.get_all_categories()
        return {"categories": categories}, 200


class CategoryDeleteResource(Resource):

    @jwt_required(locations=["headers"])
    def delete_category(category_id: str):
        if not category_id:
            return {"error": "Missing JSON in request"}, 400
        try:
            category_delete = category_service.delete_category(category_id)
            return {"category": "deleted"}, 200
        except Exception as error:
            return {"error": str(error)}, 400


class CategoryUpdateResource(Resource):

    @jwt_required(locations=["headers"])
    def update_category(category_id: str):
        data = request.get_json()
        if not category_id:
            return {"error": "Missing JSON in request"}, 400
        try:
            category_update = category_service.update_category(category_id, data["name"])
            get_category_updated = category_service.get_category_by_id(category_update)
            response_category_data = json.loads(get_category_updated)
            return {"category updated": response_category_data}, 200
        except Exception as error:
            return {"error": str(error)}, 400

