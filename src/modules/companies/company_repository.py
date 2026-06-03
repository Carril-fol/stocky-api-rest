from modules.repository import Repository
from .company_entity import CompanyEntity

class CompanyRepository(Repository):

    def create_company(self, company_instance: CompanyEntity, session=None) -> CompanyEntity:
        return self.create_register_entity(company_instance, session=session)
    
    def update_company(self, company_instance: CompanyEntity) -> CompanyEntity:
        return self.update_register_entity(company_instance)
    
    def get_company(self, company_id: int) -> CompanyEntity:
        return self.get_register_entity(CompanyEntity, company_id)
    
    def get_company_by_email(self, email: str) -> CompanyEntity:
        with self.get_session() as session:
            result = session.query(CompanyEntity).filter(CompanyEntity.email == email).first()
            return result
        
    def get_company_by_id(self, company_id: int) -> CompanyEntity:
        return self.get_register_entity(CompanyEntity, company_id)
        