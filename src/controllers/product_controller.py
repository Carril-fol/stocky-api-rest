from flask import request, make_response, Blueprint

from services.product_service import ProductService

product_controller = Blueprint('product_controller', __name__, url_prefix='/products/api/v1')
product_service = ProductService()

@product_controller.route('/create', methods=['POST'])
def create_product():
    data = request.get_json()
    try:
        product_service.create_product(data)
        return make_response({'msg': 'Product created successfully'}, 201)
    except Exception as error:
        return make_response({'error': str(error)}, 400)
    
@product_controller.route('/get/<int:id>', methods=['GET'])
def detail_product(id: int):
    try:
        product = product_service.get_product_by_id(id)
        return make_response({'msg': product}, 200)
    except Exception as error:
        return make_response({'error': str(error)}, 400)
    
@product_controller.route('/update/<int:id>', methods=['PATCH', 'PUT'])
def update_product(id: int):
    data = request.get_json()
    try:
        product_service.update_product(id, data)
        return make_response({'msg': 'Product updated successfully'}, 200)
    except Exception as error:
        return make_response({'error': str(error)}, 400)
    
@product_controller.route('/delete/<int:id>', methods=['DELETE'])
def delete_product(id: int):
    try:
        data = {'status': 'inactive'}
        product_service.delete_product(id, data)
        return make_response({'msg': 'Product deleted successfully'}, 200)
    except Exception as error:
        return make_response({'error': str(error)}, 400)
    
@product_controller.route('/get/all', methods=['GET'])
def detail_products():
    try:
        products = list(product_service.get_products())
        return make_response({'msg': products}, 200)
    except Exception as error:
        return make_response({'error': str(error)}, 400)