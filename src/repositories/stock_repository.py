from repositories.repository import Repository
from entities.stock_entity import StockEntity

class StockRepository(Repository):
    
    def get_stock_by_id(self, id: int):
        return self.get_register_entity(StockEntity, id)

    def get_stock(self):
        return self.get_registers_entity(StockEntity)
        
    def create_stock(self, stock: StockEntity):
        return self.create_register_entity(stock)    

    def update_stock(self, stock: StockEntity):
        return self.update_register_entity(stock)
        
    def delete_stock(self, stock: StockEntity):
        return self.delete_logic_register_entity(stock)

    def get_stock_by_product_id(self, product_id: int):
        with self.get_session() as session:
            return session.query(StockEntity).filter(StockEntity.product_id == product_id).first()