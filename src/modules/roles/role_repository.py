from ..repository import Repository
from .role_entity import RoleEntity

class RoleRepository(Repository):
    
    def create_role(self, role_entity, session=None) -> RoleEntity:
        return self.create_register_entity(role_entity, session=session)
        
    def get_role_by_id(self, role_id: int) -> RoleEntity | None:
        return self.get_register_entity(RoleEntity, role_id)

    def delete_soft_role(self, role_instance: RoleEntity):
        return self.delete_logic_register_entity(role_instance)
    
    def update_role(self, role_instance: RoleEntity) -> RoleEntity:
        return self.update_register_entity(role_instance)
    
    def get_roles_from_company_id(self, company_id: int, page: int, per_page: int) -> list[RoleEntity]:
        with self.get_session() as session:
            base_query = session.query(RoleEntity).filter(
                RoleEntity.company_id == company_id
            )
            
            total = base_query.count()
            
            roles = base_query.offset(
                (page - 1) * per_page
            ).limit(
                per_page
            ).all()
            
            return roles, total

    def get_role_by_name(self, name: str) -> RoleEntity | None:
        with self.get_session() as session:
            return session.query(RoleEntity).filter(RoleEntity.name == name).first()