from models.product_model import ProductModel
from entities.product_entity import ProductEntity
from repositories.product_repository import ProductRepository
from services.service import BaseService

class ProductService(BaseService):

    def __init__(self):
        self._product_model = ProductModel()
        self._product_repository = ProductRepository()

    def _product_exist(self, id: int):
        product = self._product_repository.get_product_by_id(id)
        if not product:
            raise Exception("Product not found.")
        return product
    
    def _validate_status_change(self, product, new_status: str):
        if product.status == new_status:
            raise Exception(f'Product already {product.status}')

    def get_product_by_id(self, id: int):
        product = self._product_exist(id)
        return self._validate_and_serialize(product, self._product_model)
    
    def get_products(self):
        products = self._product_repository.get_products()
        for product in products:
            yield self._validate_and_serialize(product, self._product_model)

    def create_product(self, data: dict):
        product_data_validated = self._prepare_to_entity(data, ProductModel)
        product_entity = ProductEntity(**product_data_validated.model_dump())
        return self._product_repository.create_product(product_entity)

    def update_product(self, id: int, data: dict):
        product = self._product_exist(id)
        self._validate_status_change(product, data["status"])
        product_to_update = self._prepare_to_entity(data, ProductModel, product)
        return self._product_repository.update_product(product_to_update)

    def delete_product(self, id: int, data: dict):
        product = self._product_exist(id)
        self._validate_status_change(product, data["status"])
        product_to_delete = self._prepare_to_entity(data, ProductModel, product)
        return self._product_repository.update_product(product_to_delete)
