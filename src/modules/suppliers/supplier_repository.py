from modules.repository import Repository
from .supplier_entity import SupplierEntity

class SupplierRepository(Repository):

    def get_suppliers_by_id(self, id: int):
        return self.get_register_entity(SupplierEntity, id)
    
    def get_suppliers(self, company_id: int):
        with self.get_session() as session:
            return session.query(SupplierEntity).filter(SupplierEntity.company_id == company_id).all()

    def create_supplier(self, supplier: SupplierEntity):
        return self.create_register_entity(supplier)
    
    def update_supplier(self, supplier: SupplierEntity):
        return self.update_register_entity(supplier)
        
    def delete_supplier(self, supplier: SupplierEntity):
        return self.delete_logic_register_entity(supplier)
    
    def get_supplier_by_name(self, name: str, company_id: int = None):
        with self.get_session() as session:
            query = session.query(SupplierEntity).filter(SupplierEntity.name == name)
            if company_id is not None:
                query = query.filter(SupplierEntity.company_id == company_id)
            return query.first()
        