import json
from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from products.services.product_service import ProductService

# Service
product_service = ProductService()

class ProductCreateResource(Resource):
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
        "quantity_product": "The quantity of the product cannot be less than 0."
    }
    ```
    """

    @jwt_required(locations=["headers"])
    def post(self):
        data = request.get_json()
        if not data:
            return {"error": "Missing JSON in request"}, 400
        try:
            product_created = product_service.create_product(
                data["name_product"],
                data["quantity_product"],
                data["price"],
                data["category_id"]
            )
            get_product_created = product_service.get_product_by_id(product_created)
            product_json = json.loads(get_product_created)
            return {"msg": "Product created", "product": product_json}, 201
        except Exception as error:
            return {"error": (str(error))}, 400


class ProductDetailByIdResource(Resource):
    """
    Example:

    GET: /products/<productId>
    ```
    Successful response (code 200 - OK):
    {
        "product": {
            "id": "Id from the product
            "name_product": "Name from the product",
            "quantity_product": "Quantity from the product",
            "price": "Price from the product",
            "category_id": "Category ID from the product"
        }
    }

    Response with errors (code 400 - BAD REQUEST):
    {
        "error": "Product not found"
    }
    ```
    """

    @jwt_required(locations=["headers"])
    def get(self, product_id: str):
        if not product_id:
            return {"error": "Missins ID in request"}, 400
        try:
            product_instance_exists = product_service.get_product_by_id(product_id)
            product_json = json.loads(product_instance_exists)
            return {"msg": product_json}, 200
        except Exception as error:
            return {"error": (str(error))}, 400


class ProductUpdateResource(Resource):
    """
    Example:

    PUT: /products/update/<productId>
    ```
    Application data:
    {
        "name_product": "Name from the product",
        "quantity_product": "Quantity from the product",
        "price": "Price from the product",
        "category_id": "Category ID from the product"
    }

    Successful response (code 200 - OK):
    {   
        "msg": "Product updated",
        "product": {
            "id": "Id from the product",
            "name_product": "Name from the product",
            "quantity_product": "Quantity from the product",
            "price": "Price from the product",
            "category_id": "Category ID from the product"
        }
    }

    Response with errors (code 404 - NOT FOUND):
    {
        "error": "Product not found"
    }
    ```
    """

    @jwt_required(locations=["headers"])
    def put(self, product_id: str):
        data = request.get_json()
        if not data:
            return {"error": "Missing JSON in request"}, 400
        if not product_id:
            return {"error": "Missing ID in request"}, 400
        try:
            product_update_instance = product_service.update_product(
                product_id, 
                data["name_product"], 
                data["quantity_product"],
                data["price"],
                data["category_id"]
            )
            get_product_update_instance = product_service.get_product_by_id(product_id)
            product_json = json.loads(get_product_update_instance)
            return {"msg": "Product updated", "product": product_json}, 200
        except Exception as error:
            return {"error": (str(error))}, 400


class ProductDeleteResource(Resource):
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

    @jwt_required(locations=["headers"])
    def delete(self, product_id: str):
        if not product_id:
            return {"error": "Missing ID in url"}, 400
        try:
            product_instance_delete = product_service.delete_product(product_id)
            return {"msg": "Product deleted"}, 200
        except Exception as error:
            return {"error": (str(error))}, 400
