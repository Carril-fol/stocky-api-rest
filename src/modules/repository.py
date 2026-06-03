from contextlib import contextmanager
from core.database import Database

class Repository:

    @contextmanager
    def get_session(self):
        with Database.session() as session:
            yield session

    def create_register_entity(self, entity, session=None):
        if session is not None:
            session.add(entity)
            session.flush()
            session.refresh(entity)
            return entity
        with Database.session() as session:
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity
    
    def update_register_entity(self, entity):
        with Database.session() as session:
            merged_entity = session.merge(entity)
            session.commit()
            session.refresh(merged_entity)
            return merged_entity
        
    def get_register_entity(self, entity, id: int):
        with Database.session() as session:
            return session.query(entity).filter(entity.id == id).first()
        
    def get_registers_entity(self, entity):
        with Database.session() as session:
            return session.query(entity).all()
        
    def delete_register_entity(self, entity):
        with Database.session() as session:
            session.delete(entity)
            session.commit()
            return True 
    
    def delete_logic_register_entity(self, entity):
        with Database.session() as session:
            merged_entity = session.merge(entity)
            session.commit()
            session.refresh(merged_entity)
            return merged_entity