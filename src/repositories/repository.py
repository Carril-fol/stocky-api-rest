from contextlib import contextmanager
from database.db import Database

class Repository:

    @contextmanager
    def get_session(self):
        session = Database.get_session()
        try:
            yield session
        finally:
            session.close()

    def check_database(self):
        with self.get_session() as session:
            return session.execute("SELECT 1")

    def create_register_entity(self, entity):
        with self.get_session() as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity
    
    def update_register_entity(self, entity):
        with self.get_session() as session:
            merged_entity = session.merge(entity)
            session.commit()
            session.refresh(merged_entity)
            return merged_entity
        
    def get_register_entity(self, entity, id: int):
        with self.get_session() as session:
            return session.query(entity).filter(entity.id == id).first()
        
    def get_registers_entity(self, entity):
        with self.get_session() as session:
            return session.query(entity).all()
        
    def delete_register_entity(self, entity):
        with self.get_session() as session:
            session.delete(entity)
            session.commit()
            return True 
    
    def delete_logic_register_entity(self, entity):
        with self.get_session() as session:
            merged_entity = session.merge(entity)
            session.commit()
            session.refresh(merged_entity)
            return merged_entity