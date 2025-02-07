from flask import request, make_response, Blueprint

from services.category_service import CategoryService

category_controller = Blueprint('category_controller', __name__, url_prefix='/categories/api/v1')
category_service = CategoryService()

@category_controller.route('/create', methods=['POST'])
def create_category():
    """
    Example:

    POST: /categories/api/v1/create
    ```
    Application data:
    {
        "name": "Name from the category"
    }

    Successful response (Code 201 - CREATED):
    {
        'msg': 'Category created successfully'
    }
    ```
    """
    data = request.get_json()
    try:
        category_service.create_category(data)
        return make_response({'msg': 'Category created successfully'}, 201)
    except Exception as error:
        return make_response({'msg': str(error)}, 400)

@category_controller.route('/get/<int:id>', methods=['GET'])
def get_category_by_id(id: int):
    """
    Example:

    GET: /categories/api/v1/get/<int:id>
    ```
    Successful response (Code 20O - OK):
    {
        'category': {
            'id': X,
            'name': 'Name from the category',
            'status': 'Status from the category'
        }
    }

    Error response (Code 400 - BAD REQUEST):
    {
        'msg': 'Category not found'
    }
    ```
    """
    try:
        category = category_service.get_category_by_id(id)
        return make_response({'category': category}, 200)
    except Exception as error:
        return make_response({'msg': str(error)}, 400)

@category_controller.route('/get/all', methods=['GET'])
def get_all_categories():
    """
    Example:

    GET: /categories/api/v1/get/all
    ```
    Successful response (Code 200 - OK):
    {
        'category': [
            {
                'id': X,
                'name': 'Name from the category',
                'status': 'active'
            },
            ...
        ]
    }
    ```
    """
    try:
        categories = list(category_service.get_all_categories())
        return make_response({'categories': categories}, 200)
    except Exception as error:
        return make_response({'msg': str(error)}, 400)
    
@category_controller.route('/update/<int:id>', methods=['PUT', 'PATCH'])
def update_category(id: int):
    """
    Example:

    PATH or PUT: /categories/api/v1/update/<int:id>
    ```
    Application data:
    {
        'name': 'New name from the category',
        'status': 'New status from the category'
    }

    Successful response (Code 200 - OK):
    {
        'msg': 'Category updated successfully'
    }
    ```
    """
    data = request.get_json()
    try:
        category_service.update_category(id, data)
        return make_response({'msg': 'Category updated successfully'}, 200)
    except Exception as error:
        return make_response({'msg': str(error)}, 400)
    
@category_controller.route('/delete/<int:id>', methods=['DELETE'])
def delete_category(id: int):
    """
    Example:

    DELETE: /categories/api/v1/delete/<int:id>
    ```
    Successful response (Code 200 - OK):
    {
        'msg': 'Category deleted successfully'
    }
    ```
    """
    data = {"status": "inactive"}
    try:
        category_service.delete_category(id, data)
        return make_response({'msg': 'Category deleted successfully'}, 200)
    except Exception as error:
        return make_response({'msg': str(error)}, 400)