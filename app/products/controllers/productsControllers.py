import json
from flask import request, jsonify, Blueprint
from flask_jwt_extended import jwt_required as jwtRequired

from ..repositories.productRepository import ProductRepository
from ..dao.productDao import ProductDAO
from ..services.productService import ProductService
from ..schemas.productSchemas import ProductSchema

# Service
productDao = ProductDAO()
productService = ProductService(ProductRepository(productDao))

# Blueprint
productBlueprint = Blueprint("products", __name__)


@productBlueprint.route("/products/create", methods=["POST"])
@jwtRequired(locations=["headers"])
def createProducts():
    """
    Example:

    POST: /products/create

    ```
    Application data:
    {
        "nameProduct": "Name from product",
        "quantityProduct": "Quantity from the product",
    }

    Successful response (code 201 - CREATED):
    {
        "msg": "Product created",
        "product": {
            "id": "Id from the product",
            "nameProduct": "Name from the product",
            "quantityProduct": "Quantity from the product"
        }
    }

    Response with errors from schema (code 400 - BAD REQUEST):
    {
        "cantProduct": "The quantity of the product cannot be less than 0."
    }
    ```
    """
    schema = ProductSchema()

    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON in request"}), 400
                
    errors = schema.validate(data)
    if errors:
        return jsonify({"error": errors}), 400
        
    productCreated = productService.createProduct(
        data["nameProduct"],
        data["quantityProduct"]
    )
    getProductCreated = productService.getProductById(productCreated)
    productJson = json.loads(getProductCreated.json())
    return jsonify({"msg": "Product created", "product": productJson}), 201


@productBlueprint.route("/products/<productId>", methods=["GET"])
@jwtRequired(locations=["headers"])
def getProductById(productId: str):
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
    productInstanceExists = productService.getProductById(productId)
    if not productInstanceExists:
        return jsonify({"error": "Product not found"}), 404
    
    productJson = json.loads(productInstanceExists.json())
    return jsonify({"product": productJson}), 200


@productBlueprint.route("/products/update/<productId>", methods=["PUT", "PATCH"])
@jwtRequired(locations=["headers"])
def updateProduct(productId: str):
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
    
    productUpdateInstance = productService.updateProduct(
        productId, 
        data["nameProduct"], 
        data["quantityProduct"]
    )
    getProductUpdatedInstance = productService.getProductById(productId)
    productJson = json.loads(getProductUpdatedInstance.json())
    return jsonify({"msg": "Product updated", "product": productJson}), 200


@productBlueprint.route("/products/delete/<productId>", methods=["DELETE"])
@jwtRequired(locations=["headers"])
def deletePost(productId: str):
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
    if not productId:
        return jsonify({"error": "Missing ID in url"}), 400
    
    productInstanceDelete = productService.deleteProduct(productId)
    return jsonify({"msg": "Product deleted"}), 200