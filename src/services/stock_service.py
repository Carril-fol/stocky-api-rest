from .service import BaseService
from repositories.stock_repository import StockRepository
from models.stock_model import StockModel
from entities.stock_entity import StockEntity
from exceptions.stock_exceptions import StockNotFound, StockHasAlreadyStatus

class StockService(BaseService):

    def __init__(self):
        self._stock_repository = StockRepository()
        self._stock_model = StockModel()

    def _stock_exist(self, id: int):
        stock = self._stock_repository.get_stock_by_id(id)
        if not stock:
            raise StockNotFound()
        return stock

    def _stock_by_product_id_exist(self, product_id: int):
        stock = self._stock_repository.get_stock_by_product_id(product_id)
        if not stock:
            return False
        return stock
    
    def _validate_status_in_stock(self, stock: StockEntity, data: dict):
        if stock.status == data["status"]:
            raise StockHasAlreadyStatus()

    def get_all_stock(self):
        stock = self._stock_repository.get_stock()
        for register in stock:
            validated_stock = self._validate_entity_and_serialize(register, self._stock_model)
            yield validated_stock

    def get_stock_by_id(self, id: int):
        stock = self._stock_exist(id)
        return self._validate_entity_and_serialize(stock, self._stock_model)

    def create_stock(self, data: dict, product_created_model_dump: dict):
        data['product_id'] = product_created_model_dump.get('id')
        stock_data_validated = self._prepare_to_entity(data, StockModel)
        stock_entity = StockEntity(**stock_data_validated.model_dump())
        return self._stock_repository.create_stock(stock_entity)
    
    def update_stock(self, id: int, data: dict):
        stock = self._stock_exist(id)
        stock_to_update = self._prepare_to_entity(data, self._stock_model, stock)
        return self._stock_repository.update_stock(stock_to_update)
    
    def delete_stock(self, id: int, data: dict):
        stock = self._stock_exist(id)
        self._validate_status_in_stock(stock, data)
        stock_to_delete = self._prepare_to_entity(data, self._stock_model, stock)
        return self._stock_repository.delete_stock(stock_to_delete)

    def delete_stock_by_product_id(self, product_id: int):
        data = {'status': 'inactive'}
        stock = self._stock_by_product_id_exist(product_id)
        if stock:
            stock_to_delete = self._prepare_to_entity(data, self._stock_model, stock)
            return self._stock_repository.delete_stock(stock_to_delete)