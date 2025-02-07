from flask import request, make_response, Blueprint
from services.product_service import ProductService

product_controller = Blueprint('product_controller', __name__, url_prefix='/products/api/v1')
product_service = ProductService()

@product_controller.route('/create', methods=['POST'])
def create_product():
    """
    Example:

    POST: /products/api/v1/create
    ```
    Application data:
    {
        'name': 'Name from the product',
        'description': 'Description from the product',
        'category_id': 'Id from the category to relacionate with the product',
        'quantity': 'A number to set the quantity of the product in stock table'
    }

    Successful response (Code 201 - CREATED):
    {
        'msg': 'Product created successfully'
    }
    ```
    """
    data = request.get_json()
    try:
        product_service.create_product_with_stock(data)
        return make_response({'msg': 'Product created successfully'}, 201)
    except Exception as error:
        return make_response({'error': str(error)}, 400)
    
@product_controller.route('/get/<int:id>', methods=['GET'])
def detail_product(id: int):
    """
    Example:

    GET: /products/api/v1/get/<int:id>
    ```
    Successful response (Code 200 - OK):
    {
        'product': {
            'id': 'Id from the product',
            'name': 'Name from the product',
            'description': 'Description from the product',
            'status': 'Status from the product',
            'category_id': 'Id from the category to relacionate with the product',
        }
    }
    ```
    """
    try:
        product = product_service.get_product_by_id(id)
        return make_response({'product': product}, 200)
    except Exception as error:
        return make_response({'error': str(error)}, 400)
    
@product_controller.route('/update/<int:id>', methods=['PATCH', 'PUT'])
def update_product(id: int):
    """
    Example:

    PUT or PATCH: /products/api/v1/update/<int:id>
    ```
    Application data:
    {
        'name': 'New name from the product',
        'description': 'New description from the product',
        'status': 'New status from the product',
        'category_id': 'New id from the category to relacionate with the product',
    }

    Successful response (Code 200 - OK):
    {
        'msg': 'Product updated successfully'
    }
    ```
    """
    data = request.get_json()
    try:
        product_service.update_product(id, data)
        return make_response({'msg': 'Product updated successfully'}, 200)
    except Exception as error:
        return make_response({'error': str(error)}, 400)
    
@product_controller.route('/delete/<int:id>', methods=['DELETE'])
def delete_product(id: int):
    """
    Example:

    DELETE: /products/api/v1/delete/<int:id>
    ```
    Successful response (Code 200 - OK):
    {
        'msg': 'Product deleted successfully'
    }
    ```
    """
    data = {'status': 'inactive'}
    try:
        product_service.delete_product(id, data)
        return make_response({'msg': 'Product deleted successfully'}, 200)
    except Exception as error:
        return make_response({'error': str(error)}, 400)
    
@product_controller.route('/get/all', methods=['GET'])
def detail_products():
    """
    Example:

    GET: /products/api/v1/get/all
    ```
    Successful response (Code 200 - OK):
    {
        'products': [
            {
                'id': 'Id from the product',
                'name': 'Name from the product',
                'description': 'Description from the product',
                'status': 'Status from the product',
                'category_id': 'Id from the category to relacionate with the product'
            },
            ...
        ]
    }
    ```
    """
    try:
        products = list(product_service.get_products())
        return make_response({'products': products}, 200)
    except Exception as error:
        return make_response({'error': str(error)}, 400)