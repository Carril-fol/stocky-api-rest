from flask import request, Blueprint, make_response
from flask_jwt_extended import jwt_required
from spectree import Response

from core.extensions import spectree
from .company_orchestrator import company_service
from .company_model import (
    UpdateCompanyInput,
    UpdateCompanyOutput,
    DetailCompanyModel,
    ErrorOutput
)

from ..users_companies.auth_helpers import get_current_user_company

company_controller = Blueprint(
    'company_controller',
    __name__,
    url_prefix='/companies/api/v1'
)

# --------------------------------------------------------
# Endpoints
# --------------------------------------------------------

@company_controller.route('/update/<int:company_id>', methods=['PUT', 'PATCH'])
@jwt_required()
@spectree.validate(
    json=UpdateCompanyInput,
    resp=Response(
        HTTP_200=UpdateCompanyOutput,
        HTTP_400=ErrorOutput
    )
)
def update_company(json: UpdateCompanyInput, company_id: int):
    data = json.model_dump()
    user_data = get_current_user_company()
    requesting_role_id = user_data.role_id

    company_service.update_company(company_id, data, requesting_role_id)
    return make_response({"msg": "Company updated successfully"}, 200)


@company_controller.route('/detail/<int:company_id>', methods=['GET'])
@jwt_required()
@spectree.validate(
    resp=Response(
        HTTP_200=DetailCompanyModel,
        HTTP_400=ErrorOutput
    )
)
def detail_company(company_id: int):
    user_data = get_current_user_company()
    requesting_role_id = user_data.role_id

    company_detail = company_service.detail_company(company_id, requesting_role_id)
    return make_response(company_detail, 200)