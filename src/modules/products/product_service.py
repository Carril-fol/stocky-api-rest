from ..service import BaseService

from .product_entity import ProductEntity
from .product_repository import ProductRepository
from .products_exceptions import ProductNotFound, ProductHasAlreadyStatus
from .product_model import ProductModel, BaseProductModel

from ..stock.stock_entity import StockEntity
from ..stock.stock_repository import StockRepository
from ..stock.stock_model import CreateStockModel


class ProductService(BaseService):

    def __init__(self, 
            product_repository: ProductRepository, 
            stock_repository: StockRepository
        ):
        self._product_repository = product_repository
        self._stock_repository = stock_repository
    
    # --------------------------------------------------------
    # Helpers
    # --------------------------------------------------------

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

    def _create_stock(self, data: dict, product_data_dict: dict) -> StockEntity:
        stock_data = {**data, "product_id": product_data_dict.get("id")}
        stock_entity = StockEntity(**CreateStockModel.model_validate(stock_data).model_dump())
        return self._stock_repository.create_stock(stock_entity)

    def _to_product_dict(self, product: ProductEntity):
        return ProductModel.model_validate(product.to_dict()).model_dump(by_alias=True)

    # --------------------------------------------------------
    # Public functions
    # --------------------------------------------------------

    def get_product_by_id(self, id: int) -> dict:
        product_entity = self._product_exist_by_id(id)
        return self._to_product_dict(product_entity)
    
    def get_products(self, company_id: int, page: int, per_page: int, search: str = None) -> list[dict]:
        products_db, total = self._product_repository.get_products(company_id, page, per_page, search)
        products = [ self._to_product_dict(product) for product in products_db]
        return products, total

    def create_product(self, data: dict, company_id: int) -> ProductEntity:
        data["company_id"] = company_id

        product_data_validated = BaseProductModel.model_validate(data).model_dump()
        product_entity = ProductEntity(**product_data_validated)

        product_created = self._product_repository.create_product(product_entity)
        product_created_model_dump = self._to_product_dict(product_created)
        
        self._create_stock(data, product_created_model_dump)
        return product_created

    def update_product(self, id: int, data: dict) -> ProductEntity:
        product = self._product_exist_by_id(id)
        self._validate_status_change(product, data)
        
        product_model_validated_data = BaseProductModel.model_validate(data).model_dump(exclude_unset=True)
        product_to_update = self._update_instance_entity(product_model_validated_data, product)
        return self._product_repository.update_product(product_to_update)

    def deactivate_product(self, id: int, data: dict) -> ProductEntity:
        product = self._product_exist_by_id(id)
        self._validate_status_change(product, data)

        product_to_deactivate = self._update_instance_entity(data, product)
        product_deactivated = self._product_repository.update_product(product_to_deactivate)

        self._deactivate_stock_for_product(id)
        return product_deactivated

    def _deactivate_stock_for_product(self, product_id: int) -> None:
        stock = self._stock_repository.get_stock_by_product_id(product_id)
        if stock and stock.quantity != 0:
            stock.quantity = 0
            self._stock_repository.update_stock(stock)

    def get_products_by_category_id(self, company_id: int, id: int) -> list[dict]:
        products_by_category = []
        for product_entity in self._product_repository.get_products_by_category_id(company_id, id):
            product_dict = self._to_product_dict(product_entity)
            products_by_category.append(product_dict)
        return products_by_category
    
    def get_product_by_name(self, name: str, company_id: int) -> ProductEntity:
        name = str.upper(name)
        product = self._product_repository.get_product_by_name(name, company_id)
        
        if not product:
            raise ProductNotFound()

        return self._to_product_dict(product)