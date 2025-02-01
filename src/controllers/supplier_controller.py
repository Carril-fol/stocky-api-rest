from flask import Blueprint, make_response, request

from models.supplier_model import SupplierModel
from services.supplier_service import SupplierService

supplier_controller = Blueprint('supplier_controller', __name__, url_prefix='/suppliers/api/v1')
supplier_service = SupplierService()
supplier_model = SupplierModel()

@supplier_controller.route('/create', methods=['POST'])
def create_supplier():
    data = request.get_json()
    try:
        supplier_service.create_supplier(data)
        return make_response({'msg': 'Supplier created successfully'}, 201)
    except Exception as error:
        return make_response({'error': str(error)}, 400)

@supplier_controller.route('/get/<int:id>', methods=['GET'])
def detail_supplier(id: int):
    try:
        supplier = supplier_service.get_supplier_by_id(id)
        return make_response({'supplier': supplier}, 200)
    except Exception as error:
        return make_response({'error': str(error)}, 400)
    
@supplier_controller.route('/delete/<int:id>', methods=['DELETE'])
def delete_supplier(id: int):
    data = {'status': 'inactive'}
    try:
        supplier_service.delete_supplier(id, data)
        return make_response({'msg': 'Supplier deleted successfully'}, 200)
    except Exception as error:
        return make_response({'error': str(error)}, 400)
    
@supplier_controller.route('/get/all', methods=['GET'])
def get_suppliers():
    try:
        suppliers = list(supplier_service.get_suppliers())
        return make_response({'suppliers': suppliers}, 200)
    except Exception as error:
        return make_response({'error': str(error)}, 400)
    
@supplier_controller.route('/update/<int:id>', methods=['PUT', 'PATCH'])
def update_supplier(id: int):
    data = request.get_json()
    try:
        supplier_service.update_supplier(id, data)
        return make_response({'msg': 'Supplier updated successfully'}, 200)
    except Exception as error:
        return make_response({'error': str(error)}, 400)