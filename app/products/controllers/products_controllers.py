import json
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required

from ..repositories.product_repository import ProductRepository
from ..dao.product_dao import ProductDao
from ..services.product_service import ProductService

# Dao
product_dao = ProductDao()

# Service
product_service = ProductService(ProductRepository(product_dao))

# Blueprint
product_blueprint = Blueprint("products", __name__)

@product_blueprint.route("/products/create", methods=["POST"])
@jwt_required(locations=["headers"])
def create_products():
    """
    Example:

    POST: /products/create

    ```
    Application data:
    {
        "name_product": "Name from product",
        "quantity_product": "Quantity from the product",
        "price": "Price from the product",
        "category_id": Id from the category to the product.
    }

    Successful response (code 201 - CREATED):
    {
        "msg": "Product created",
        "product": {
            "id": "Id from the product",
            "name_product": "Name from product",
            "quantity_product": "Quantity from the product",
            "price": "Price from the product",
            "category_id": "Id from the category to the product"
        }
    }

    Response with errors from model (code 400 - BAD REQUEST):
    {
        "cantProduct": "The quantity of the product cannot be less than 0."
    }
    ```
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON in request"}), 400
    try:
        product_created = product_service.create_product(
            data["name_product"],
            data["quantity_product"]
        )
        get_product_created = product_service.get_product_by_id(product_created)
        product_json = json.loads(get_product_created.json())
        return jsonify({"msg": "Product created", "product": product_json}), 201
    except Exception as error:
        return jsonify({"error": (str(error))}), 400

@product_blueprint.route("/products/<product_id>", methods=["GET"])
@jwt_required(locations=["headers"])
def get_product_by_id(product_id: str):
    """
    Example:

    GET: /products/<productId>

    ```
    Successful response (code 200 - OK):
    {
        "product": {
            "id": "Id from the product",
            "nameProduct": "Name from the product",
            "quantityProduct": "Quantity from the product"
        }
    }

    Response with errors (code 404 - NOT FOUND):
    {
        "error": "Product not found"
    }
    ```
    """
    if not product_id:
        return jsonify({"error": "Missins ID in request"}), 400
    try:
        product_instance_exists = product_service.get_product_by_id(product_id)
        product_json = json.loads(product_instance_exists.json())
        return jsonify({"msg": product_json}), 200
    except Exception as error:
        return jsonify({"error": (str(error))}), 400

@product_blueprint.route("/products/update/<product_id>", methods=["PUT", "PATCH"])
@jwt_required(locations=["headers"])
def update_product(product_id: str):
    """
    Example:

    GET: /products/update/<productId>

    ```
    Application data:
    {
        "nameProduct": "New name from product",
        "quantityProduct": "New quantity from product",
    }

    Successful response (code 200 - OK):
    {   
        "msg": "Product updated",
        "product": {
            "nameProduct": "Name from the product",
            "quantityProduct": "Quantity from the post",
        }
    }

    Response with errors (code 404 - NOT FOUND):
    {
        "error": "Post not found"
    }
    ```
    """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON in request"}), 400
    try:
        product_update_instance = product_service.update_product(
            product_id, 
            data["name_product"], 
            data["quantity_product"],
            data["price"],
            data["category_id"]
        )
        get_product_update_instance = product_service.get_product_by_id(product_id)
        product_json = json.loads(get_product_update_instance.json())
        return jsonify({"msg": "Product updated", "product": product_json}), 200
    except Exception as error:
        return jsonify({"error": (str(error))}), 400

@product_blueprint.route("/products/delete/<product_id>", methods=["DELETE"])
@jwt_required(locations=["headers"])
def delete_product(product_id: str):
    """
    Example:

    GET: /products/delete/<productId>

    ```
    Successful response (code 200 - OK):
    {   
        "msg": "Product deleted"
    }

    Response with errors (code 400 - BAD REQUEST):
    {
        "error": "Missing ID in url"
    }
    ```
    """
    if not product_id:
        return jsonify({"error": "Missing ID in url"}), 400
    try:
        product_instance_delete = product_service.delete_product(product_id)
        return jsonify({"msg": "Product deleted"}), 200
    except Exception as error:
        return jsonify({"error": (str(error))}), 400
