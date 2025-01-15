from models.product_model import ProductModel
from entities.product_entity import ProductEntity
from repositories.product_repository import ProductRepository

class ProductService:

    def __init__(self):
        self._product_model = ProductModel()
        self._product_repository = ProductRepository()

    def _prepare_product_entity(self, data: dict, product: ProductEntity = None):
        validated_data = self._product_model.model_validate(data)
        if product:
            for key, value in data.items():
                setattr(product, key, value)
            return product
        return validated_data

    def _product_exist(self, id: int):
        product = self._product_repository.get_product_by_id(id)
        if not product:
            raise Exception("Product not found.")
        return product
    
    def get_product_by_id(self, id: int):
        product = self._product_exist(id)
        product_dump = self._product_model.model_validate(product.__dict__).model_dump(by_alias=True)
        return product_dump
    
    def get_products(self):
        products = self._product_repository.get_products()
        for product in products:
            product_validated = self._product_model.model_validate(product.__dict__).model_dump(by_alias=True)
            yield product_validated

    def create_product(self, data: dict):
        product_data_validated = self._prepare_product_entity(data)
        product_entity = ProductEntity(**product_data_validated.model_dump())
        return self._product_repository.create_product(product_entity)

    def update_product(self, id: int, data: dict):
        product = self._product_exist(id)
        product_to_update = self._prepare_product_entity(data, product)
        return self._product_repository.update_product(product_to_update)

    def delete_product(self, id: int):
        product = self._product_exist(id)
        if product.status == 'inactive':
            raise Exception('Product already inactive.')
        data = {'status': 'inactive'}
        product_to_delete = self._prepare_product_entity(data, product)
        return self._product_repository.update_product(product_to_delete)