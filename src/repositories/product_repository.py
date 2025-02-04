from repositories.repository import Repository
from entities.product_entity import ProductEntity

class ProductRepository(Repository):

    def get_product_by_id(self, id: int):
        return self.get_register_entity(ProductEntity, id)
        
    def get_products(self):
        return self.get_registers_entity(ProductEntity)
    
    def create_product(self, product: ProductEntity):
        return self.create_register_entity(product)
    
    def update_product(self, product: ProductEntity):
        return self.update_register_entity(product)
    
    def delete_logic_product(self, product: ProductEntity):
        return self.delete_logic_register_entity(product)
    
    def get_products_by_category_id(self, id: int):
        with self.get_session() as session:
            products = session.query(ProductEntity).filter(ProductEntity.category_id == id).all()
            return products