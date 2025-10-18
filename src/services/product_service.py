from .service import BaseService

from entities.product_entity import ProductEntity
from entities.stock_entity import StockEntity
from entities.supplier_entity import SupplierEntity

from repositories.product_repository import ProductRepository
from repositories.stock_repository import StockRepository
from repositories.supplier_repository import SupplierRepository

from models.product_model import ProductModel, CreateProductModel, UpdateProductModel
from models.stock_model import CreateStockModel
from models.supplier_model import SupplierModel

from exceptions.products_exceptions import ProductNotFound, ProductHasAlreadyStatus


class ProductService(BaseService):

    def __init__(self, product_repository: ProductRepository, stock_repository: StockRepository, supplier_repository: SupplierRepository):
        self._product_repository = product_repository
        self._stock_repository = stock_repository
        self._supplier_repository = supplier_repository

    def _product_exist_by_id(self, id: int) -> ProductNotFound | ProductEntity:
        product = self._product_repository.get_product_by_id(id)
        if not product:
            raise ProductNotFound()
        return product
    
    def _validate_status_change(self, product: ProductEntity, data: dict) -> ProductHasAlreadyStatus | ProductEntity:
        status = data.get("status") 
        if status is not None and status == product.status:
            raise ProductHasAlreadyStatus()
        return product

    def _get_default_supplier(self) -> SupplierEntity:
        name = "SIN PROVEEDOR"
        supplier = self._supplier_repository.get_supplier_by_name(name)
        return supplier

    def _create_stock(self, data: dict, product_data_dict: dict) -> StockEntity:
        data['product_id'] = product_data_dict.get('id')
        stock_dict = CreateStockModel.model_validate(data).model_dump()

        stock_entity = StockEntity(**stock_dict)
        return self._stock_repository.create_stock(stock_entity)

    def get_product_by_id(self, id: int) -> dict:
        product = self._product_exist_by_id(id)
        return ProductModel.model_validate(product.to_dict()).model_dump(by_alias=True)
    
    def get_products(self) -> list[dict]:
        products = []
        for product in self._product_repository.get_products():
            product_model_dump = ProductModel.model_validate(product.to_dict()).model_dump(by_alias=True)
            products.append(product_model_dump)
        return products

    def create_product(self, data: dict) -> ProductEntity:
        supplier_id = data.get("supplier_id")

        if not supplier_id:
            supplier_instance = self._get_default_supplier()
            data["supplier_id"] = supplier_instance.id

        product_data_validated = CreateProductModel.model_validate(data).model_dump()
        product_entity = ProductEntity(**product_data_validated)

        product_created = self._product_repository.create_product(product_entity)
        product_created_model_dump = ProductModel.model_validate(product_created.to_dict()).model_dump()
        self._create_stock(data, product_created_model_dump)
        return product_created

    def update_product(self, id: int, data: dict) -> ProductEntity:
        product = self._product_exist_by_id(id)
        self._validate_status_change(product, data)
        
        product_model_validated_data = UpdateProductModel.model_validate(data).model_dump(by_alias=True, exclude_unset=True)
        product_to_update = self._update_instance_entity(product_model_validated_data, product)
        return self._product_repository.update_product(product_to_update)

    def delete_product(self, id: int, data: dict) -> ProductEntity:
        product = self._product_exist_by_id(id)
        self._validate_status_change(product, data)
        
        self._stock_service.delete_stock_by_product_id(id)
        product_to_delete = self._update_instance_entity(data, product)
        return self._product_repository.update_product(product_to_delete)

    def get_products_by_category_id(self, id: int) -> list[dict]:
        products_by_category = []
        for product in self._product_repository.get_products_by_category_id(id):
            product_model_validated_data = ProductModel.model_validate(product.to_dict()).model_dump(by_alias=True)
            products_by_category.append(product_model_validated_data)
        return products_by_category