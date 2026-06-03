from ..repository import Repository
from .users_companies_entity import UsersCompaniesEntity

class UsersCompaniesRepository(Repository):
    
    def create_user_company_role(self, user_company_entity: UsersCompaniesEntity, session=None):
        return self.create_register_entity(user_company_entity, session=session)
    
    def delete_user_company_role(self, user_company_entity: UsersCompaniesEntity):
        return self.delete_register_entity(user_company_entity)

    def get_user_company_role_by_user_id(self, user_id: int):
        with self.get_session() as session:
            return session.query(
                UsersCompaniesEntity
            ).filter(
                UsersCompaniesEntity.user_id == user_id
            ).first()
    
    def get_users_by_role_id(self, role_id: int) -> list[UsersCompaniesEntity]:
        with self.get_session() as session:
            return session.query(
                UsersCompaniesEntity
            ).filter(
                UsersCompaniesEntity.role_id == role_id
            ).all()

    def get_users_by_company_id(self, company_id: int) -> list[UsersCompaniesEntity]:
        with self.get_session() as session:
            return session.query(
                UsersCompaniesEntity
            ).filter(
                UsersCompaniesEntity.company_id == company_id
            ).all()

    def update_user_company_role(self, user_comapny_entity: UsersCompaniesEntity):
        return self.update_register_entity(user_comapny_entity)