from ..repositories.category_repository import CategoryRepository
from ..domain.category_model import CategoryModel

class CategoryService:
    """
    
    """
    def __init__(self, category_repository: CategoryRepository):
        self.category_repository =  category_repository

    def __category_exists_by_name(self, name: str) -> bool:
        """
        Check if a category with the given name exists.

        Args:
        ----
        name (str): The name of the category to check.

        Returns:
        -------
        bool: `True` if the category exists, `False` otherwise.
        """
        category_exists = self.category_repository.get_category_by_name(name)
        return bool(category_exists)
    
    def __category_exists_by_id(self, category_id: str) -> bool:
        """
        Check if a category with the given name exists.

        Args:
        ----
        name (str): The name of the category to check.

        Returns:
        -------
        bool: `True` if the category exists, `False` otherwise.
        """
        category_exists = self.category_repository.get_category_by_id(category_id)
        return True if category_exists else None
        
    def create_category(self, name: str):
        """
        Create a new category.

        Args:
        ----
        name (str): The name of the new category.

        Returns:
        -------
        dict: The newly created category data.

        Raises:
        ------
        Exception: If a category with the given name already exists.
        """
        if self.__category_exists_by_name(name):
            raise Exception("A category with this name already exists.")
        category_model_instance = CategoryModel(name=name.lower())
        return self.category_repository.create_category(category_model_instance)
    
    def get_category_by_name(self, name: str):
        """
        Retrieve a category by its name.

        Args:
        ----
        name (str): The name of the category to retrieve.

        Returns:
        -------
        CategoryModel: An instance of `CategoryModel` with the category's data.

        Raises:
        ------
        Exception: If a category with the given name does not exist.
        """
        if not self.__category_exists_by_name(name):
            raise Exception("Category does not exist.")
        category = self.category_repository.get_category_by_name(name)
        return CategoryModel(name=category["name"])
    
    def get_category_by_id(self, category_id: str):
        """
        Retrieve a category by its ID.

        Args:
        ----
        category_id (str): The ID of the category to retrieve.

        Returns:
        -------
        CategoryModel: An instance of `CategoryModel` with the category's data.

        Raises:
        ------
        Exception: If a category with the given ID does not exist.
        """
        if not self.__category_exists_by_id(category_id):
            raise Exception("Category not found.")
        category = self.category_repository.get_category_by_id(category_id)
        return CategoryModel(name=category["name"])
    
    def get_all_categories(self):
        """
        Retrieve all categories.

        Returns:
        -------
        list: A list of dictionaries, each containing category data.
        """
        categories = self.category_repository.get_categories()
        return [
            {
                "id": str(category["_id"]),
                "name": category["name"]
            }
            for category in categories
        ]

    def update_category(self, category_id: str, name_category: str):
        """
        Update a category's name.

        Args:
        ----
        category_id (str): The ID of the category to update.
        name_category (str): The new name for the category.

        Returns:
        -------
        str: The ID of the updated category.

        Raises:
        ------
        Exception: If the category with the given ID does not exist.
        """
        if not self.__category_exists_by_id(category_id):
            raise Exception("Category not found.")
        
        category_model_instance = CategoryModel(name=name_category.lower())
        self.category_repository.update_category(category_id, category_model_instance)
        return category_id
    
    def delete_category(self, category_id: str):
        """
        Delete a category by its ID.

        Args:
        ----
        category_id (str): The ID of the category to delete.

        Returns:
        -------
        dict: The result of the delete operation.

        Raises:
        ------
        Exception: If the category with the given ID does not exist.
        """
        if not self.__category_exists_by_id(category_id):
            raise Exception("Category not found.")
        
        return self.category_repository.delete_category(category_id)
