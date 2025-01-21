from repositories.repository import Repository
from entities.supplier_entity import SupplierEntity

class SupplierRepository(Repository):

    def get_suppliers_by_id(self, id: int):
        return self.get_register_entity(SupplierEntity, id)
    
    def get_suppliers(self):
        return self.get_registers_entity(SupplierEntity)

    def create_supplier(self, supplier: SupplierEntity):
        return self.create_register_entity(supplier)
    
    def update_supplier(self, supplier: SupplierEntity):
        return self.update_register_entity(supplier)
        
    def delete_supplier(self, supplier: SupplierEntity):
        return self.delete_logic_register_entity(supplier)
    
    def get_supplier_by_name(self, name: str):
        with self.get_session() as session:
            return session.query(SupplierEntity).filter(SupplierEntity.name == name).first()
        