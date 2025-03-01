import pandas as pd
from io import BytesIO
from .service import BaseService

from models.product_model import ProductModel
from repositories.stock_repository import StockRepository
from models.stock_model import StockModel, StockProductDetail
from entities.stock_entity import StockEntity
from exceptions.stock_exceptions import StockNotFound, StockHasAlreadyStatus

class StockService(BaseService):

    def __init__(self):
        self.stock_repository = StockRepository()
        self._stock_model = StockModel()
        self._stock_product_detail_model = StockProductDetail()

    def _stock_exist(self, id: int):
        stock = self.stock_repository.get_stock_detailed_by_id(id)
        if not stock:
            raise StockNotFound()
        return stock

    def _stock_by_product_id_exist(self, product_id: int):
        stock = self.stock_repository.get_stock_by_product_id(product_id)
        if not stock:
            return False
        return stock
    
    def _validate_status_in_stock(self, stock: StockEntity, data: dict):
        if stock.status == data["status"]:
            raise StockHasAlreadyStatus()

    def get_stock_by_id(self, id: int):
        stock = self._stock_exist(id)
        register_stock = self._validate_entity_and_serialize(stock[0], self._stock_model)
        register_product = self._validate_entity_and_serialize(stock[1], ProductModel)
        return {"stock": register_stock, "product": register_product}

    def create_stock(self, data: dict, product_created_model_dump: dict):
        data['product_id'] = product_created_model_dump.get('id')
        stock_data_validated = self._prepare_to_entity(data, StockModel)
        stock_entity = StockEntity(**stock_data_validated.model_dump())
        return self.stock_repository.create_stock(stock_entity)
    
    def update_stock(self, id: int, data: dict):
        stock = self._stock_exist(id)[0]
        stock_to_update = self._prepare_to_entity(data, self._stock_model, stock)
        return self.stock_repository.update_stock(stock_to_update)
    
    def delete_stock(self, id: int, data: dict):
        stock = self._stock_exist(id)[0]
        self._validate_status_in_stock(stock, data)
        stock_to_delete = self._prepare_to_entity(data, self._stock_model, stock)
        return self.stock_repository.delete_stock(stock_to_delete)

    def delete_stock_by_product_id(self, product_id: int):
        data = {'status': 'inactive'}
        stock = self._stock_by_product_id_exist(product_id)
        if stock:
            stock_to_delete = self._prepare_to_entity(data, self._stock_model, stock)
            return self.stock_repository.delete_stock(stock_to_delete)
        
    def get_stock_low(self):
        stock = self.stock_repository.get_stock_low_quantity()
        for register in stock:
            yield self._validate_entity_and_serialize(register, self._stock_model)

    def get_stock_detailed_with_product(self, page, per_page):
        stocks = []
        stock = self.stock_repository.get_stock_detailed(page, per_page)
        for register in stock:
            register_stock = self._validate_entity_and_serialize(register[0], self._stock_model)
            register_product = self._validate_entity_and_serialize(register[1], ProductModel)
            data = {
                'stock': register_stock,
                'product': register_product
            }
            stocks.append(data)
        return stocks

    def report_excel_stock_with_all_products(self):
        data_array = []
        stock = self.stock_repository.get_stock_detailed_all()
        for register in stock:
            data = self._stock_product_detail_model.model_validate(register).model_dump()
            data_array.append(data)
        df = pd.DataFrame(data_array)
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name='stock_report')
        output.seek(0)
        return output