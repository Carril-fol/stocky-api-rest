from contextlib import contextmanager
from database.db import Database
from entities.supplier_entity import SupplierEntity

class SupplierRepository:

    @contextmanager
    def get_session(self):
        session = Database.get_session()
        try:
            yield session
        finally:
            session.close()

    def get_suppliers_by_id(self, id: int):
        with self.get_session() as session:
            return session.query(SupplierEntity).filter(SupplierEntity.id == id).first()
    
    def get_supplier_by_name(self, name: str):
        with self.get_session() as session:
            return session.query(SupplierEntity).filter(SupplierEntity.name == name).first()
        
    def get_suppliers(self):
        with self.get_session() as session:
            return session.query(SupplierEntity).all()

    def create_supplier(self, supplier: SupplierEntity):
        with self.get_session() as session:
            session.add(supplier)
            session.commit()
            session.refresh(supplier)
            return supplier
    
    def update_supplier(self, supplier: SupplierEntity):
        with self.get_session() as session:
            merged_supplier = session.merge(supplier)
            session.commit()
            session.refresh(merged_supplier)
            return merged_supplier
        
    def delete_supplier(self, supplier: SupplierEntity):
        with self.get_session() as session:
            merged_supplier = session.merge(supplier)
            session.commit()
            session.refresh(merged_supplier)
            return merged_supplier