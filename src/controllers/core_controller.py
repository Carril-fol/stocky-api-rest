from flask import make_response, Blueprint

from services.core_service import CoreService

core_controller = Blueprint('core_controller', __name__, url_prefix='/core/api/v1')
core_service = CoreService()

@core_controller.route('/status', methods=['GET'])
def check_status():
    status_db = core_service.check_status_database
    return make_response({"status": "Ok", "database": "Connected" if status_db else "Disconnected"}, 200)
    