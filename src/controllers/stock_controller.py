from flask import Blueprint, request, make_response
from services.stock_service import StockService

stock_controller = Blueprint('stock_controller', __name__, url_prefix='/stock/api/v1')
stock_service = StockService()

@stock_controller.route('/', methods=['GET'])
def get_all_stock():
    """
    Example:

    GET: /stock/api/v1/
    ```
    Parameters data:
    {
        page: Number of the page.
        per_page: Number of elements to show per page.
    }

    Successful response (Code 200 - OK):
    {
        'data': [
            'stock': {
                'id': 'Id from the stock',
                'product_id': 'Id from the product',
                'quantity': 'Quantity from the product in stock',
                'status': 'Status from the stock',
            },
            'product': {
                'id': 'Id from the product',
                'name': 'Name from the product',
                'description': 'Description from the product',
                'status': 'Status from the product',
                'category_id': 'Id from the category to relacionate with the product',
            }
            ...
        ]
    }
    ```
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    try:
        data = stock_service.get_stock_detailed_with_product(page, per_page)
        return make_response({'data': data}, 200)
    except Exception as error:
        return make_response({'error': str(error)}, 400)

@stock_controller.route('/get/<int:id>', methods=['GET'])
def get_stock_by_id(id: int):
    """
    Example:

    GET: /stock/api/v1/get/<int:id>
    ```
    Successful response (Code 200 - OK):
    {
        'stock': {
            'id': 'Id from the stock',
            'product_id': 'Id from the product',
            'quantity': 'Quantity from the product in stock',
            'status': 'Status from the stock',
        }
    }
    ```
    """
    try:
        stock = stock_service.get_stock_by_id(id)
        return make_response({'data': stock}, 200)
    except Exception as error:
        return make_response({'error': str(error)}, 400)

@stock_controller.route('/update/<int:id>', methods=['PUT', 'PATCH'])
def update_stock(id: int):
    """
    Example:

    PUT or PATCH: /stock/api/v1/update/<int:id>
    ```
    Application data:
    {
        'product_id': 'Id from the product',
        'quantity': 'Quantity from the product in stock',
        'status': 'Status from the stock',
    }

    Successful response (Code 200 - OK):
    {
        'msg': 'Stock updated successfully'
    }
    ```
    """
    data = request.get_json()
    try:
        stock_service.update_stock(id, data)
        return make_response({'msg': 'Stock updated successfully'}, 200)
    except Exception as error:
        return make_response({'error': str(error)}, 400)
    
@stock_controller.route('/delete/<int:id>', methods=['DELETE'])
def delete_stock(id: int):
    """
    Example:
    
    DELETE: /stock/api/v1/delete/<int:id>
    ```
    Successful response (Code 200 - OK):
    {
        'msg': 'Stock deleted successfully'
    }
    ```
    """
    data = {'status': 'inactive'}
    try:
        stock_service.delete_stock(id, data)
        return make_response({'msg': 'Stock deleted successfully'}, 200)
    except Exception as error:
        return make_response({'error': str(error)}, 400)
    
@stock_controller.route('/low')
def get_low_stock():
    """
    Example:
    
    GET: /stock/api/v1/low
    ```
    Successful response (Code 200 - OK):
    {
        'stock': [
            {
                'id': 'Id from the stock',
                'product_id': 'Id from the product',
                'quantity': 'Quantity from the product in stock',
                'status': 'Status from the stock',
            },
            ...
        ]
    }
    ```
    """
    data = list(stock_service.get_stock_low())
    return make_response({'data': data}, 200)

