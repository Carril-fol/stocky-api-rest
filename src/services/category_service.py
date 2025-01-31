from models.category_model import CategoryModel
from entities.category_entity import CategoryEntity
from repositories.category_repository import CategoryRepository
from exceptions.categories_exceptions import (
    CategoryNotFound,
    CategoryAlreadyExists,
    CategoryStatusError
)

from .service import BaseService

class CategoryService(BaseService):

    def __init__(self):
        self._category_repository = CategoryRepository()
        self._category_model = CategoryModel()

    def _category_exists_by_id(self, id: int):
        category = self._category_repository.get_category_by_id(id)
        if not category:
            raise CategoryNotFound()
        return category

    def _category_exists_by_name(self, name: str):
        category = self._category_repository.get_category_by_name(name)
        if category:
            raise CategoryAlreadyExists()

    def _validate_status_in_category(self, category, status: str):
        if category.status == status:
            raise CategoryStatusError()
        return category

    def get_category_by_id(self, id: int):
        category = self._category_exists_by_id(id)
        return self._validate_and_serialize(category, self._category_model)

    def create_category(self, data: dict):
        self._category_exists_by_name(data['name'])
        validated_data = self._prepare_to_entity(data, CategoryModel)
        category_to_create = CategoryEntity(**validated_data.model_dump())
        return self._category_repository.create_category(category_to_create)
    
    def get_all_categories(self):
        for category in self._category_repository.get_categories():
            validated_category = self._validate_and_serialize(category, self._category_model)
            yield validated_category

    def update_category(self, id: int, data: dict):
        category = self._category_exists_by_id(id)
        category_updated = self._prepare_to_entity(data, None, category)
        return self._category_repository.update_category(category_updated)
    
    def delete_category(self, id: int, data: dict):
        category = self._category_exists_by_id(id)
        self._validate_status_in_category(category, data['status'])
        category_to_delete = self._prepare_to_entity(data, category)
        return self._category_repository.delete_category(category_to_delete)