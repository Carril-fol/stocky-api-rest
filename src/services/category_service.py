from .service import BaseService
from .product_service import ProductService

from models.category_model import CategoryModel
from entities.category_entity import CategoryEntity
from repositories.category_repository import CategoryRepository
from exceptions.categories_exceptions import (
    CategoryNotFound,
    CategoryAlreadyExists,
    CategoryStatusError
)

class CategoryService(BaseService):

    def __init__(self):
        self._category_repository = CategoryRepository()
        self._category_model = CategoryModel()
        self._product_service = ProductService()

    def _find_category(self, category_id: int):
        category = self._category_repository.get_category_by_id(category_id)
        if not category:
            raise CategoryNotFound()
        return category

    def _validate_unique_name(self, data: dict):
        if self._category_repository.get_category_by_name(data["name"]):
            raise CategoryAlreadyExists()

    def _validate_status_in_category(self, category, data: dict):
        if category.status == data["status"]:
            raise CategoryStatusError()

    def _get_or_create_default_category(self):
        data = {'name': 'other', 'status': 'active'}
        return self._category_repository.get_category_by_name('other') or self.create_category(data)
    
    def _change_category_if_is_deleted(self, id: int):
        default_category_id = self._get_or_create_default_category()
        data = {'category_id': default_category_id.id}
        for product in self._product_service.get_product_by_category_id(id):
            self._product_service.update_product(product['id'], data)

    def get_category_by_id(self, id: int):
        category = self._find_category(id)
        return self._validate_entity_and_serialize(category, self._category_model)

    def create_category(self, data: dict):
        self._validate_unique_name(data)
        validated_data = self._prepare_to_entity(data, CategoryModel)
        category_to_create = CategoryEntity(**validated_data.model_dump())
        return self._category_repository.create_category(category_to_create)
    
    def get_all_categories(self):
        for category in self._category_repository.get_categories():
            yield self._validate_entity_and_serialize(category, self._category_model)

    def update_category(self, id: int, data: dict):
        category = self._find_category(id)
        category_updated = self._prepare_to_entity(data, self._category_model, category)
        return self._category_repository.update_category(category_updated)
    
    def delete_category(self, id: int, data: dict):
        category = self._find_category(id)
        self._validate_status_in_category(category, data)
        self._change_category_if_is_deleted(id)
        category_to_delete = self._prepare_to_entity(data, self._category_model, category)
        return self._category_repository.delete_category(category_to_delete)
