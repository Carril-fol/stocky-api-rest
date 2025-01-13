from models.category_model import CategoryModel
from entities.category_entity import CategoryEntity
from repositories.category_repository import CategoryRepository

class CategoryService:

    def __init__(self):
        self.category_repository = CategoryRepository()
        self.category_model = CategoryModel()

    def _category_exists(self, category_model: CategoryModel):
        categories = self.category_repository.get_categories()
        for category in categories:
            if category.name == category_model.name:
                return category
        return False

    def _format_data_into_model(self, data: dict):
        return self.category_model.model_validate(data)
    
    def _format_data_into_category_exist(self, data: dict, category: CategoryEntity):
        for key, value in data.items():
            setattr(category, key, value)
        return category

    def get_category_by_id(self, id: int):
        category = self.category_repository.get_category_by_id(id)
        if not category:
            raise Exception("Category not found")
        return self.category_repository.get_category_by_id(id)

    def create_category(self, data: dict):
        validated_data = self._format_data_into_model(data)
        category_exists = self._category_exists(validated_data)
        if category_exists:
            if category_exists.status == 'inactive':
                raise Exception('Category already exists but inactive')
            raise Exception('Category already exists and is active')
        category_to_create = CategoryEntity(**validated_data.model_dump())
        return self.category_repository.create_category(category_to_create)
    
    def get_all_categories(self):
        for category in self.category_repository.get_categories():
            validated_category = self.category_model.model_validate(category.__dict__).model_dump(by_alias=True)
            yield validated_category

    def update_category(self, id: int, data: dict):
        category = self.category_repository.get_category_by_id(id)
        if not category:
            raise Exception('Category not found')
        category_updated = self._format_data_into_category_exist(data, category)
        return self.category_repository.update_category(category_updated)
    
    def delete_category(self, id: int):
        category = self.category_repository.get_category_by_id(id)
        if not category:
            raise Exception('Category not found')
        elif category.status == 'inactive':
            raise Exception('Category already inactive')
        data = {"status": "inactive"}
        category_to_delete = self._format_data_into_category_exist(data, category)
        return self.category_repository.delete_category(category_to_delete)