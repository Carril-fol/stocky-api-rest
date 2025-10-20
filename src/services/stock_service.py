from .service import BaseService

from entities.stock_entity import StockEntity
from entities.product_entity import ProductEntity

from models.product_model import ProductModel, UpdateProductModel
from models.stock_model import StockDetail, CreateStockModel, UpdateStockModel

from repositories.stock_repository import StockRepository
from repositories.product_repository import ProductRepository

from exceptions.stock_exceptions import StockNotFound, StockHasAlreadyStatus
from exceptions.products_exceptions import ProductNotFound


class StockService(BaseService):

    def __init__(self, stock_repository: StockRepository, product_repository: ProductRepository):
        self.stock_repository = stock_repository
        self.product_repository = product_repository

    def _get_stock_by_id_or_none(self, id: int) -> StockNotFound | StockEntity:
        stock = self.stock_repository.get_stock_by_id(id)
        if not stock:
            raise StockNotFound()
        return stock

    def _get_product_by_id_or_none(self, id: int) -> ProductNotFound | ProductEntity:
        product = self.product_repository.get_product_by_id(id)
        if not product:
            raise ProductNotFound()
        return product

    def _get_stock_by_product_id_exist(self, product_id: int) -> StockNotFound | StockEntity:
        stock = self.stock_repository.get_stock_by_product_id(product_id)
        if not stock:
            return StockNotFound()
        return stock
    
    def _validate_status_in_stock(self, stock: StockEntity, data: dict):
        if stock.status == data["status"]:
            raise StockHasAlreadyStatus()

    def get_stock_by_id(self, id: int) -> dict:
        stock_instance = self._get_stock_by_id_or_none(id)
        stock_model_dump = StockDetail.model_validate(stock_instance.to_dict()).model_dump()
        
        product_instance = self._get_product_by_id_or_none(stock_instance.product_id)
        product_model_dump = ProductModel.model_validate(product_instance.to_dict()).model_dump()
        return {"stock": stock_model_dump, "product": product_model_dump}

    def create_stock(self, data: dict, product_created_model_dump: dict) -> StockEntity:
        data['product_id'] = product_created_model_dump.get('id')
        stock_model_instance = CreateStockModel.model_validate(data).model_dump()

        stock_entity = StockEntity(**stock_model_instance)
        return self.stock_repository.create_stock(stock_entity)
    
    def update_stock(self, id: int, data: dict) -> StockEntity:
        stock = self._get_stock_by_id_or_none(id)
        stock_model_dump = UpdateStockModel.model_validate(data).model_dump(exclude_unset=True)

        stock_to_update = self._update_instance_entity(stock_model_dump, stock)
        return self.stock_repository.update_stock(stock_to_update)
    
    def delete_stock(self, id: int, data: dict) -> StockEntity:
        stock = self._get_stock_by_id_or_none(id)
        stock_model_dump = UpdateStockModel.model_validate(data).model_dump(exclude_unset=True)
        self._validate_status_in_stock(stock, stock_model_dump)

        product_data = {"status": "inactive"}
        product_instance = self.product_repository.get_product_by_id(stock.product_id)
        product_model_dump = UpdateProductModel.model_validate(product_data).model_dump(exclude_unset=True)

        stock_to_delete = self._update_instance_entity(stock_model_dump, stock)
        product_to_update = self._update_instance_entity(product_model_dump, product_instance)

        self.product_repository.update_product(product_to_update)
        return self.stock_repository.delete_stock(stock_to_delete)

    def delete_stock_by_product_id(self, product_id: int) -> StockEntity:
        data = {'status': 'inactive'}
        stock = self._get_stock_by_product_id_exist(product_id)
        stock_model_dump = UpdateStockModel.model_validate(data).model_dump(exclude_unset=True)

        stock_entity_updated = self._update_instance_entity(stock_model_dump, stock)
        return self.stock_repository.delete_stock(stock_entity_updated)
        
    def get_stock_low(self) -> list[dict]:
        stock_list = []
        stock = self.stock_repository.get_stock_low_quantity()
        for register in stock:
            stock_instance = StockDetail.model_validate(register.to_dict()).model_dump()
            stock_list.append(stock_instance)
        return stock_list

    def get_stock_detailed_with_product(self, page, per_page) -> list[dict]:
        stocks = []
        registers = self.stock_repository.get_stock_detailed(page, per_page)
        for register in registers:
            stock = StockDetail.model_validate(register[0].to_dict()).model_dump()
            product = ProductModel.model_validate(register[1].to_dict()).model_dump()
            data = {"stock": stock, "product": product}
            stocks.append(data)
        return stocks

    # def report_excel_stock_with_all_products(self):
    #     data_array = []
    #     stock = self.stock_repository.get_stock_detailed_all()
    #     for register in stock:
    #         data = self._stock_product_detail_model.model_validate(register).model_dump()
    #         data_array.append(data)
    #     df = pd.DataFrame(data_array)
    #     output = BytesIO()
    #     with pd.ExcelWriter(output, engine="openpyxl") as writer:
    #         df.to_excel(writer, index=False, sheet_name='stock_report')
    #     output.seek(0)
    #     return output