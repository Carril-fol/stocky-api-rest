from modules.repository import Repository
from .product_entity import ProductEntity


class ProductRepository(Repository):

    def get_product_by_id(self, id: int):
        return self.get_register_entity(ProductEntity, id)
        
    def get_products(
        self,
        company_id: int,
        page: int = 1,
        per_page: int = 10,
        search: str = None
    ):
        with self.get_session() as session:
            query = session.query(ProductEntity)\
                .filter(ProductEntity.company_id == company_id)

            if search:
                query = query.filter(ProductEntity.name.ilike(f"%{search}%"))

            total = query.count()

            products = query\
                .offset((page - 1) * per_page)\
                .limit(per_page)\
                .all()

            return products, total

    def create_product(self, product: ProductEntity):
        return self.create_register_entity(product)
    
    def update_product(self, product: ProductEntity):
        return self.update_register_entity(product)
    
    def delete_logic_product(self, product: ProductEntity):
        return self.delete_logic_register_entity(product)
    
    def get_products_by_category_id(self, company_id: int, id: int):
        with self.get_session() as session:
            products = session.query(
                ProductEntity
            ).filter(
                ProductEntity.category_id == id, 
                ProductEntity.company_id == company_id
            ).all()
            return products

    def get_product_by_name(self, name: str, company_id: int):
        with self.get_session() as session:
            product = session.query(
                ProductEntity
            ).filter(
                ProductEntity.name == name, 
                ProductEntity.company_id == company_id
            ).first()
            return product
        
    