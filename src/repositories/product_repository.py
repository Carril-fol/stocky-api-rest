from contextlib import contextmanager

from database.db import Database
from entities.product_entity import ProductEntity

class ProductRepository:

    @contextmanager
    def get_session(self):
        session = Database.get_session()
        try:
            yield session
        finally:
            session.close()

    def get_product_by_id(self, id: int):
        with self.get_session() as session:
            return session.query(ProductEntity).filter(ProductEntity.id == id).first() 
        
    def get_products(self):
        with self.get_session() as session:
            return session.query(ProductEntity).all()
    
    def create_product(self, product: ProductEntity):
        with self.get_session() as session:
            session.add(product)
            session.commit()
            session.refresh(product)
            return product
    
    def update_product(self, product: ProductEntity):
        with self.get_session() as session:
            merged_product = session.merge(product)
            session.commit()
            session.refresh(merged_product)
            return merged_product