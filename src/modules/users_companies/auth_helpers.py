from flask_jwt_extended import get_jwt_identity
from .users_companies_repository import UsersCompaniesRepository
from .users_companies_entity import UsersCompaniesEntity

users_companies_repo = UsersCompaniesRepository()


def get_current_user_company() -> UsersCompaniesEntity:
    user_id = int(get_jwt_identity())
    return users_companies_repo.get_user_company_role_by_user_id(user_id)
