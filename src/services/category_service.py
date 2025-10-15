from .service import BaseService
from .product_service import ProductService

from models.category_model import CategoryModel, CreateOrUpdateCategoryModel
from entities.category_entity import CategoryEntity
from repositories.category_repository import CategoryRepository
from repositories.product_repository import ProductRepository
from exceptions.categories_exceptions import CategoryNotFound, CategoryAlreadyExists, CategoryStatusError


class CategoryService(BaseService):

    def __init__(self, category_respository: CategoryRepository, product_repository: ProductRepository):
        self._category_repository = category_respository
        self._product_repository = product_repository

    def _find_category(self, category_id: int) -> CategoryEntity:
        category = self._category_repository.get_category_by_id(category_id)
        if not category:
            raise CategoryNotFound()
        return category

    def _validate_unique_name(self, data: dict) -> CategoryAlreadyExists | None:
        if self._category_repository.get_category_by_name(data["name"]):
            raise CategoryAlreadyExists()

    def _validate_status_in_category(self, category: CategoryEntity, data: dict) -> CategoryStatusError | None:
        if category.status == data["status"]:
            raise CategoryStatusError()

    def _get_or_create_default_category(self) -> CategoryEntity:
        data = {'name': 'other', 'status': 'active'}
        return self._category_repository.get_category_by_name('other') or self.create_category(data)
    
    def _change_category_if_is_deleted(self, id: int):
        default_category_id = self._get_or_create_default_category()
        data = {'category_id': default_category_id.id}
        
        for product in self._product_repository.get_products_by_category_id(id):
            product_updated = self._update_instance_entity(data, product)
            self._product_repository.update_product(product_updated)

    def get_category_by_id(self, id: int) -> dict:
        category = self._find_category(id)
        return CategoryModel.model_validate(category.to_dict()).model_dump()

    def create_category(self, data: dict) -> CategoryEntity:
        self._validate_unique_name(data)
        validated_data = CreateOrUpdateCategoryModel.model_validate(data)

        category_to_create = CategoryEntity(**validated_data.model_dump())
        return self._category_repository.create_category(category_to_create)
    
    def get_all_categories(self) -> list[dict]:
        categories = []
        for category in self._category_repository.get_categories():
            category_dumped = CategoryModel.model_validate(category.to_dict()).model_dump(by_alias=True)
            categories.append(category_dumped)
        return categories

    def update_category(self, id: int, data: dict) -> CategoryEntity:
        category = self._find_category(id)
        category_validated = CreateOrUpdateCategoryModel.model_validate(category.to_dict()).model_dump(by_alias=True)

        category_updated = self._update_instance_entity(category_validated, category)
        return self._category_repository.update_category(category_updated)
    
    def delete_category(self, id: int, data: dict) -> CategoryEntity:
        category = self._find_category(id)
        self._validate_status_in_category(category, data)
        self._change_category_if_is_deleted(id)

        category_to_delete = self._update_instance_entity(data, category)
        return self._category_repository.delete_category(category_to_delete)
