from flask import request, make_response, Blueprint

from repositories.product_repository import ProductRepository
from repositories.stock_repository import StockRepository
from repositories.supplier_repository import SupplierRepository

from services.product_service import ProductService

stock_repository = StockRepository()
product_repository = ProductRepository()
supplier_repository = SupplierRepository()

product_service = ProductService(product_repository, stock_repository, supplier_repository)
product_controller = Blueprint("product_controller", __name__, url_prefix="/products/api/v1")

@product_controller.route("/create", methods=["POST"])
def create_product():
    """
    Create a new product along with its initial stock.

    Method: POST
    URL: /products/api/v1/create

    Request Body:
    {
        "name": "Product name",
        "description": "Product description",
        "category_id": "ID of the associated category",
        "quantity": "Initial stock quantity"
    }

    Successful Response (201 CREATED):
    {
        "msg": "Product created successfully"
    }

    Error Response (400 BAD REQUEST):
    {
        "error": "Error description"
    }
    """
    data = request.get_json()
    try:
        product_service.create_product(data)
        return make_response({"msg": "Product created successfully"}, 201)
    except Exception as error:
        return make_response({"error": str(error)}, 400)

@product_controller.route("/get/<int:id>", methods=["GET"])
def detail_product(id: int):
    """
    Retrieve product details by ID.

    Method: GET
    URL: /products/api/v1/get/<id>

    Path Parameters:
        id (int): The ID of the product to retrieve

    Successful Response (200 OK):
    {
        "product": {
            "id": "Product ID",
            "name": "Product name",
            "description": "Product description",
            "status": "Product status",
            "category_id": "ID of the associated category"
        }
    }

    Error Response (400 BAD REQUEST):
    {
        "error": "Error description"
    }
    """
    if not id:
        return make_response({"error": "ID not provided"}, 400)

    try:
        product = product_service.get_product_by_id(id)
        return make_response({"product": product}, 200)
    except Exception as error:
        return make_response({"error": str(error)}, 400)

@product_controller.route("/update/<int:id>", methods=["PATCH", "PUT"])
def update_product(id: int):
    """
    Update an existing product.

    Methods: PUT, PATCH
    URL: /products/api/v1/update/<id>

    Path Parameters:
        id (int): The ID of the product to update

    Request Body:
    {
        "name": "New product name",
        "description": "New product description",
        "status": "New product status",
        "category_id": "New ID of the associated category"
    }

    Successful Response (200 OK):
    {
        "msg": "Product updated successfully"
    }

    Error Response (400 BAD REQUEST):
    {
        "error": "Error description"
    }
    """
    if not id:
        return make_response({"error": "ID not provided"}, 400)

    data = request.get_json()
    try:
        product_service.update_product(id, data)
        return make_response({"msg": "Product updated successfully"}, 200)
    except Exception as error:
        return make_response({"error": str(error)}, 400)

@product_controller.route("/delete/<int:id>", methods=["DELETE"])
def delete_product(id: int):
    """
    Soft-delete a product by marking it as inactive.

    Method: DELETE
    URL: /products/api/v1/delete/<id>

    Path Parameters:
        id (int): The ID of the product to delete

    Successful Response (200 OK):
    {
        "msg": "Product deleted successfully"
    }

    Error Response (400 BAD REQUEST):
    {
        "error": "Error description"
    }

    Note: This performs a logical deletion by changing the product status to 'inactive'.
    """
    if not id:
        return make_response({"error": "ID not provided"}, 400)

    data = {"status": "inactive"}
    try:
        product_service.delete_product(id, data)
        return make_response({"msg": "Product deleted successfully"}, 200)
    except Exception as error:
        return make_response({"error": str(error)}, 400)

@product_controller.route("/get/all", methods=["GET"])
def detail_products():
    """
    Retrieve all products.

    Method: GET
    URL: /products/api/v1/get/all

    Successful Response (200 OK):
    {
        "products": [
            {
                "id": "Product ID",
                "name": "Product name",
                "description": "Product description",
                "status": "Product status",
                "category_id": "ID of the associated category"
            },
            ...
        ]
    }

    Error Response (400 BAD REQUEST):
    {
        "error": "Error description"
    }
    """
    try:
        products = list(product_service.get_products())
        return make_response({"products": products}, 200)
    except Exception as error:
        return make_response({"error": str(error)}, 400)
