from ..service import BaseService

from .category_entity import CategoryEntity
from .category_repository import CategoryRepository
from .categories_exceptions import CategoryNotFound, CategoryAlreadyExists, CategoryStatusError, CategoryNameReserved

from .category_model import CreateCategoryModel, UpdateCategoryModel, DetailCategoryModel, ListDetailCategoryModel
from ..products.product_repository import ProductRepository


RESERVED_CATEGORY_NAME = "OTHER"


class CategoryService(BaseService):

    def __init__(
            self, 
            category_respository: CategoryRepository, 
            product_repository: ProductRepository
        ):
        self._category_repository = category_respository
        self._product_repository = product_repository
        
    # --------------------------------------------------------
    # Helpers
    # --------------------------------------------------------
    
    def _format_category(self, category_entity: CategoryEntity) -> dict:
        return DetailCategoryModel.model_validate(
            category_entity.to_dict()
        ).model_dump()
        
    def _get_category_or_raise(self, category_id: int, company_id: int) -> CategoryEntity:
        category = self._category_repository.get_category_by_id(category_id, company_id)
        if not category:
            raise CategoryNotFound()
        return category

    def _validate_unique_name(self, data: dict) -> CategoryAlreadyExists | None:
        if self._category_repository.get_category_by_name(data["name"]):
            raise CategoryAlreadyExists()

    def _validate_status_in_category(self, category: CategoryEntity, data: dict) -> CategoryStatusError | None:
        if category.status == data["status"]:
            raise CategoryStatusError()
   
    def _reassign_products_to_other(self, id: int, company_id: int):
        fallback = self._category_repository.get_category_by_name(RESERVED_CATEGORY_NAME, company_id)
        products: list = self._product_repository.get_products_by_category_id(company_id, id)

        if not products or not fallback:
            return
        
        data = {'category_id': fallback.id}
        for product in products:
            product_updated = self._update_instance_entity(data, product)
            self._product_repository.update_product(product_updated)

    # --------------------------------------------------------
    # Public functions
    # --------------------------------------------------------

    def create_default_category(self) -> CategoryEntity:
        data = {'name': RESERVED_CATEGORY_NAME, 'status': 'ACTIVE'}
        category_model = CreateCategoryModel.model_validate(data)
        category_exist = self._category_repository.get_category_by_name(category_model.name)

        if not category_exist:
            category_model_dump = category_model.model_dump()
            category_entity = CategoryEntity(**category_model_dump)
            self._category_repository.create_category(category_entity)

    def get_category_by_id(self, id: int, company_id: int) -> dict:
        category = self._get_category_or_raise(id, company_id)
        return self._format_category(category)

    def create_category(self, data: dict, company_id: int) -> CategoryEntity:
        if data.get("name", "").upper() == RESERVED_CATEGORY_NAME:
            raise CategoryNameReserved()

        data["company_id"] = company_id

        category_model_dump = CreateCategoryModel.model_validate(data).model_dump()
        category_entity = CategoryEntity(**category_model_dump)
        return self._category_repository.create_category(category_entity)
    
    def get_all_categories_from_company(self, company_id: int, page: int, per_page: int ) -> ListDetailCategoryModel:
        categories_db, total = self._category_repository.get_categories_by_company_id(company_id, page, per_page)

        categories = [ self._format_category(category) for category in categories_db]
        return categories, total

    def update_category(self, id: int, data: dict, company_id: int) -> CategoryEntity:
        category = self._get_category_or_raise(id, company_id)
        data["company_id"] = category.company_id
        category_model_dump = UpdateCategoryModel.model_validate(
            data
        ).model_dump(
            exclude_unset=True
        )

        category_entity = self._update_instance_entity(category_model_dump, category)
        return self._category_repository.update_category(category_entity)
    
    def delete_category(self, id: int, data: dict, company_id: int) -> CategoryEntity:
        category_instance = self._get_category_or_raise(id, company_id)
        self._validate_status_in_category(category_instance, data)
        self._reassign_products_to_other(id, company_id)

        category_entity = self._update_instance_entity(data, category_instance)
        return self._category_repository.delete_category(category_entity)

    def get_category_by_name(self, name: str, company_id: int) -> DetailCategoryModel:
        name_formatted = name.upper()
    
        category = self._category_repository.get_category_by_name(name_formatted, company_id)
        if not category:
            raise CategoryNotFound()
        
        return self._format_category(category)
