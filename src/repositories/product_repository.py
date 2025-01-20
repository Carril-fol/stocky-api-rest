from repositories.repository import Repository
from entities.product_entity import ProductEntity

class ProductRepository(Repository):

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