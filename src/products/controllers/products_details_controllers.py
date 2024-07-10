import json
from flask import request
from flask_restful import Resource

from products.services.product_detail_service import ProductDetailService

# Services
product_detail_service = ProductDetailService()


class ProductDetailCreateResource(Resource):
    """
    Example:

    POST: /products/details/create

    ```
    Application data:
    {
        "product_id": "Id from product father",
        "barcode": "barcode from the product",
        "status": "Status from the product"
    }

    Successful response (code 201 - CREATED):
    {
        "msg": "Product detail created",
        "product detail": {
            "id": "Id from the product detail",
            "product_id": "Id from the product father",
            "barcode": "Barcode from the product detail",
            "status": "Status from the product"
        }
    }

    ```
    """
    def post(self):
        data = request.get_json()
        if not data:
            return {"error": "Missing JSON in the request"}, 400
        try:
            product_detail_created = product_detail_service.create_product_detail(
                data["product_id"],
                data["barcode"],
                data["status"]
            )
            product_detail_instance = product_detail_service.get_product_detail_by_barcode(product_detail_created.barcode).model_dump_json()
            response_data_product_detail = json.loads(product_detail_instance)
            return {"msg": "Product detail created", "product detail": response_data_product_detail}, 201
        except Exception as error:
            return {"error": str(error)}, 400
        

class ProductDetailGetResource(Resource):
    
    def get(self, barcode: str):
        try:
            product_details_instance = product_detail_service.get_product_detail_by_barcode(barcode).model_dump_json()
            response_data_product_detail = json.loads(product_details_instance)
            return {"product": response_data_product_detail}, 200
        except Exception as error:
            return {"error": str(error)}, 400
        

class ProductDetailUpdateResource(Resource):

    def patch(self, barcode: str):
        data = request.get_json()
        if not data:
            return {"error": "Missing JSON in the request"}, 400
        if not barcode:
            return {"error": "Missing barcode in the request"}, 400
        try:
            product_detail_update = product_detail_service.update_product_detail(
            data["barcode"],
            data["status"]
        )
            produdct_detail_updated = product_detail_service.get_product_detail_by_barcode(barcode).model_dump_json()
            response_product_detail_data = json.loads(produdct_detail_updated)
            return {"product": response_product_detail_data}, 200
        except Exception as error:
            return {"error": str(error)}, 400
        

class ProductDetailDeleteResource(Resource):
    
    def delete(self, barcode: str):
        if not barcode:
            return {"error": "Missing barcode in the request"}, 400
        try:
            product_detail_delete = product_detail_service.delete_product_detail(barcode)
            return {"product": "deleted"}, 200
        except Exception as error:
            return {"error": str(error)}, 400