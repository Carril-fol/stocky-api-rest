from repositories.repository import Repository
from entities.stock_entity import StockEntity
from entities.product_entity import ProductEntity

class StockRepository(Repository):
            
    def create_stock(self, stock: StockEntity):
        return self.create_register_entity(stock)    

    def update_stock(self, stock: StockEntity):
        return self.update_register_entity(stock)
        
    def delete_stock(self, stock: StockEntity):
        return self.delete_logic_register_entity(stock)

    def get_stock_by_product_id(self, product_id: int):
        with self.get_session() as session:
            return session.query(StockEntity).filter(StockEntity.product_id == product_id)

    def get_stock_low_quantity(self):
        with self.get_session() as session:
            return session.query(StockEntity).filter(StockEntity.quantity < 10).all()
        
    def get_stock_detailed(self, page, per_page):
        with self.get_session() as session:
            query = session.query(StockEntity, ProductEntity).join(ProductEntity, StockEntity.product_id == ProductEntity.id)
            return query.limit(per_page).offset((page - 1) * per_page).all()

    def get_stock_detailed_by_id(self, id: int):
        with self.get_session() as session:
            return session.query(StockEntity, ProductEntity).join(ProductEntity, StockEntity.product_id == ProductEntity.id).filter(StockEntity.id == id).first()
        
    def get_stock_detailed_all(self):
        with self.get_session() as session:
            query = session.query(
                StockEntity.id, StockEntity.product_id, StockEntity.quantity, StockEntity.status, StockEntity.date_updated,
                ProductEntity.name, ProductEntity.description, ProductEntity.category_id, ProductEntity.status, ProductEntity.date_creation, ProductEntity.date_updated
            ).join(ProductEntity, StockEntity.product_id == ProductEntity.id)
            results = query.all()
            column_names = [desc["name"] for desc in query.column_descriptions]
            return [dict(zip(column_names, row)) for row in results]
