from repositories.repository import Repository
from entities.stock_entity import StockEntity

class StockRepository(Repository):
    
    def get_stock_by_id(self, id: int):
        with self.get_session() as session:
            return session.query(StockEntity).filter(StockEntity.id == id).first()
    
    def get_stock(self):
        with self.get_session() as session:
            return session.query(StockEntity).all()
        
    def create_stock(self, stock: StockEntity):
        with self.get_session() as session:
            session.add(stock)
            session.commit()
            session.refresh(stock)
            return stock

    def update_stock(self, stock: StockEntity):
        with self.get_session() as session:
            merged_stock = session.merge(stock)
            session.commit()
            session.refresh(merged_stock)
            return merged_stock
        
    def delete_stock(self, stock: StockEntity):
        with self.get_session() as session:
            merged_stock = session.merge(stock)
            session.commit()
            session.refresh(merged_stock)
            return merged_stock