import json
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

from ..dao.category_dao import CategoryDao
from ..repositories.category_repository import CategoryRepository
from ..services.category_service import CategoryService

# Dao
category_dao = CategoryDao()

# Service
category_service = CategoryService(CategoryRepository(category_dao))

# Blueprint
category_blueprint = Blueprint("categories", __name__)

@category_blueprint.route("/categories/create", methods=["POST"])
@jwt_required(locations=["headers"])
def register_category():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON in request"}), 400
    try:
        category_created = category_service.create_category(data["name"])
        get_category_created = category_service.get_category_by_id(category_created)
        response_category_data = json.loads(get_category_created.json())
        return jsonify({"msg": "Category created", "category": response_category_data}), 201
    except Exception as error:
        return jsonify({"msg": str(error)}), 400

@category_blueprint.route("/categories/details/<name>", methods=["GET"])
@jwt_required(locations=["headers"])
def detail_category(name: str):
    if not name:
        return jsonify({"error": "Missing JSON in request"}), 400
    try:
        category = category_service.get_category_by_name(name)
        response_category_data = json.loads(category.json())
        return jsonify({"category": response_category_data}), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 400

@category_blueprint.route("/categories", methods=["GET"])
@jwt_required(locations=["headers"])
def get_categories():
    categories = category_service.get_all_categories()
    return jsonify({"categories": categories}), 200

@category_blueprint.route("/categories/delete/<category_id>", methods=["DELETE"])
@jwt_required(locations=["headers"])
def delete_category(category_id: str):
    if not category_id:
        return jsonify({"error": "Missing JSON in request"}), 400
    try:
        category_delete = category_service.delete_category(category_id)
        return jsonify({"category": "deleted"}), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 400

@category_blueprint.route("/categories/update/<category_id>", methods=["PUT", "PATCH"])
@jwt_required(locations=["headers"])
def update_category(category_id: str):
    data = request.get_json()
    if not category_id:
        return jsonify({"error": "Missing JSON in request"}), 400
    try:
        category_update = category_service.update_category(category_id, data["name"])
        get_category_updated = category_service.get_category_by_id(category_update)
        response_category_data = json.loads(get_category_updated.json())
        return jsonify({"category updated": response_category_data}), 200
    except Exception as error:
        return jsonify({"error": str(error)}), 400
