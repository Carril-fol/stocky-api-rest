from models.product_model import ProductModel
from entities.product_entity import ProductEntity
from repositories.product_repository import ProductRepository
from exceptions.products_exceptions import (
    ProductNotFound,
    ProductHasAlreadyStatus
)

from .service import BaseService
from .stock_service import StockService

class ProductService(BaseService):

    def __init__(self):
        self._product_model = ProductModel()
        self._product_repository = ProductRepository()
        self._stock_service = StockService()

    def _product_exist(self, id: int):
        product = self._product_repository.get_product_by_id(id)
        if not product:
            raise ProductNotFound()
        return product
    
    def _validate_status_change(self, product, new_status: str):
        if product.status == new_status:
            raise ProductHasAlreadyStatus()

    def get_product_by_id(self, id: int):
        product = self._product_exist(id)
        return self._validate_entity_and_serialize(product, self._product_model)
    
    def get_products(self):
        products = self._product_repository.get_products()
        for product in products:
            yield self._validate_entity_and_serialize(product, self._product_model)

    def create_product_with_stock(self, data: dict):
        product_data_validated = self._prepare_to_entity(data, ProductModel)
        product_entity = ProductEntity(**product_data_validated.model_dump())
        product_created = self._product_repository.create_product(product_entity)
        product_created_model_dump = self._validate_entity_and_serialize(product_created, self._product_model)
        return self._stock_service.create_stock(data, product_created_model_dump)

    def update_product(self, id: int, data: dict):
        product = self._product_exist(id)
        self._validate_status_change(product, data["status"])
        product_to_update = self._prepare_to_entity(data, ProductModel, product)
        return self._product_repository.update_product(product_to_update)

    def delete_product(self, id: int, data: dict):
        product = self._product_exist(id)
        self._validate_status_change(product, data["status"])
        self._stock_service.delete_stock_by_product_id(id)
        product_to_delete = self._prepare_to_entity(data, ProductModel, product)
        return self._product_repository.update_product(product_to_delete)
