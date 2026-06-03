from ..repository import Repository
from ..stock.stock_entity import StockEntity
from ..products.product_entity import ProductEntity


class StockRepository(Repository):
            
    def create_stock(self, stock: StockEntity):
        return self.create_register_entity(stock)    

    def update_stock(self, stock: StockEntity):
        return self.update_register_entity(stock)
        
    def delete_stock(self, stock: StockEntity):
        return self.delete_logic_register_entity(stock)

    def get_stock_by_product_id(self, product_id: int):
        with self.get_session() as session:
            return session.query(StockEntity).filter(StockEntity.product_id == product_id).first()

    def get_stock_low_quantity(self, page: int, per_page: int, company_id: int):
        with self.get_session() as session:
            query = session.query(StockEntity, ProductEntity)\
                .join(ProductEntity, StockEntity.product_id == ProductEntity.id)\
                .filter(StockEntity.quantity < 10, ProductEntity.company_id == company_id)
            total = query.count()
            items = query.limit(per_page).offset((page - 1) * per_page).all()
            return items, total
        
    def get_stock_detailed(self, page: int, per_page: int, company_id: int):
        with self.get_session() as session:
            query = session.query(StockEntity, ProductEntity)\
                .join(ProductEntity, StockEntity.product_id == ProductEntity.id)\
                .filter(ProductEntity.company_id == company_id)
            total = query.count()
            items = query.limit(per_page).offset((page - 1) * per_page).all()
            return items, total

    def get_stock_by_id(self, id: int):
        return self.get_register_entity(StockEntity, id)