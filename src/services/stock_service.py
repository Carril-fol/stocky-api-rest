from .service import BaseService
from repositories.stock_repository import StockRepository
from models.stock_model import StockModel
from entities.stock_entity import StockEntity

class StockService(BaseService):

    def __init__(self):
        self._stock_repository = StockRepository()
        self._stock_model = StockModel()

    def _stock_exist(self, id: int):
        stock = self._stock_repository.get_stock_by_id(id)
        if not stock:
            raise Exception("Stock not found.")
        return stock

    def get_all_stock(self):
        stock = self._stock_repository.get_stock()
        for register in stock:
            validated_stock = self._validate_and_serialize(register, self._stock_model)
            yield validated_stock

    def get_stock_by_id(self, id: int):
        stock = self._stock_exist(id)
        return self._validate_and_serialize(stock, self._stock_model)

    def create_stock(self, data: dict, product_created_model_dump: dict):
        data['product_id'] = product_created_model_dump.get('id')
        stock_data_validated = self._prepare_to_entity(data, StockModel)
        stock_entity = StockEntity(**stock_data_validated.model_dump())
        return self._stock_repository.create_stock(stock_entity)
    
    def update_stock(self, id: int, data: dict):
        stock = self._stock_exist(id)
        stock_to_update = self._prepare_to_entity(data, StockModel, stock)
        return self._stock_repository.update_stock(stock_to_update)
    
    def delete_stock(self, id: int):
        stock = self._stock_exist(id)
        return self._stock_repository.delete_stock(stock)