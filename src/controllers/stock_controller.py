from flask import Blueprint, request, make_response

from services.stock_service import StockService

stock_controller = Blueprint('stock_controller', __name__, url_prefix='/stock/api/v1')
stock_service = StockService()

@stock_controller.route('/', methods=['GET'])
def get_all_stock():
    stock = stock_service.get_all_stock()
    return make_response({'stock': list(stock)}, 200)

@stock_controller.route('/<int:id>', methods=['GET'])
def get_stock_by_id(id: int):
    stock = stock_service.get_stock_by_id(id)
    return make_response({'stock': stock}, 200)

@stock_controller.route('/update/<int:id>', methods=['PUT', 'PATCH'])
def update_stock(id: int):
    data = request.get_json()
    try:
        stock_service.update_stock(id, data)
        return make_response({'msg': 'Stock updated successfully'}, 200)
    except Exception as error:
        return make_response({'error': str(error)}, 400)
    
@stock_controller.route('/delete/<int:id>', methods=['DELETE'])
def delete_stock(id: int):
    try:
        stock_service.delete_stock(id)
        return make_response({'msg': 'Stock deleted successfully'}, 200)
    except Exception as error:
        return make_response({'error': str(error)}, 400)