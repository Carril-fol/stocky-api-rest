from flask import Blueprint, make_response, request
from repositories.supplier_repository import SupplierRepository
from services.supplier_service import SupplierService

supplier_controller = Blueprint('supplier_controller', __name__, url_prefix='/suppliers/api/v1')
supplier_repository = SupplierRepository()
supplier_service = SupplierService(supplier_repository)

@supplier_controller.route('/create', methods=['POST'])
def create_supplier():
    """
    Example:

    POST: /suppliers/api/v1/create
    ```
    Application data:
    {
        'name': 'Name from the supplier'
    }

    Successful response (Code 201 - CREATED):
    {
        'msg': 'Supplier created successfully'
    }

    Error response (Code 400 - BAD REQUEST):
    {
        'error': 'Supplier already exists'
    }
    ```
    """
    data = request.get_json()
    try:
        supplier_service.create_supplier(data)
        return make_response({'msg': 'Supplier created successfully'}, 201)
    except Exception as error:
        return make_response({'error': str(error)}, 400)

@supplier_controller.route('/get/<int:id>', methods=['GET'])
def detail_supplier(id: int):
    """
    Example:

    POST: /suppliers/api/v1/get/<int:id>
    ```
    Successful response (Code 200 - OK):
    {
        'supplier': {
            'id': 'Id from the supplier',
            'name': 'Name from the supplier',
            'status': 'Status from the supplier'
        }
    }

    Error response (Code 400 - BAD REQUEST):
    {
        'error': 'Supplier not founded'
    }
    ```
    """
    try:
        supplier = supplier_service.get_supplier_by_id(id)
        return make_response({'supplier': supplier}, 200)
    except Exception as error:
        return make_response({'error': str(error)}, 400)
    
@supplier_controller.route('/delete/<int:id>', methods=['DELETE'])
def delete_supplier(id: int):
    """
    Example:

    POST: /suppliers/api/v1/delete/<int:id>
    ```
    Successful response (Code 200 - OK):
    {
        'msg': 'Supplier deleted successfully'
    }

    Error response (Code 400 - BAD REQUEST):
    {
        'error': 'Supplier not founded'
    }
    ```
    """
    data = {'status': 'INACTIVE'}
    try:
        supplier_service.delete_supplier(id, data)
        return make_response({'msg': 'Supplier deleted successfully'}, 200)
    except Exception as error:
        return make_response({'error': str(error)}, 400)
    
@supplier_controller.route('/', methods=['GET'])
def get_suppliers():
    """
    Example:

    POST: /suppliers/api/v1/
    ```
    Successful response (Code 200 - OK):
    {
        'suppliers': [
            {
                'id': 'Id from the supplier',
                'name': 'Name from the supplier',
                'status': 'Status from the supplier'
            }
            ...
        ]
    }
    ```
    """
    try:
        suppliers = list(supplier_service.get_suppliers())
        return make_response({'suppliers': suppliers}, 200)
    except Exception as error:
        return make_response({'error': str(error)}, 400)
    
@supplier_controller.route('/update/<int:id>', methods=['PUT', 'PATCH'])
def update_supplier(id: int):
    """
    Example:

    POST: /suppliers/api/v1/update/<int:id>
    ```
    Application data:
    {
        'name': 'New name from the supplier',
        'status: 'New status from the supplier'
    }

    Successful response (Code 200 - OK):
    {
        'msg': 'Supplier updated successfully'
    }

    Error response (Code 400 - BAD REQUEST):
    {
        'error': 'Supplier not founded'
    }
    ```
    """
    data = request.get_json()
    try:
        supplier_service.update_supplier(id, data)
        return make_response({'msg': 'Supplier updated successfully'}, 200)
    except Exception as error:
        return make_response({'error': str(error)}, 400)