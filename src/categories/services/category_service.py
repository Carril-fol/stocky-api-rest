from categories.repositories.category_repository import CategoryRepository
from categories.models.category_model import CategoryModel
from categories.exceptions.categories_exceptions import CategoryNotFound,CategoryAlreadyExists


class CategoryService:
    def __init__(self):
        """
        Initialize the class with "Category Repository" for use

        Atributes:
        ---------
        category_repository: (CategoryRepository()): Class instance of "CategoryRepository"
        """
        self.category_repository =  CategoryRepository()

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
        category_created: The ID from the catergory created.

        Raises:
        ------
        Exception: If a category with the given name already exists.
        """
        category_exists = self.__category_exists_by_name(name)
        if category_exists:
            raise CategoryAlreadyExists()
        category_model_instance = CategoryModel(name=name)
        category_created = self.category_repository.create_category(category_model_instance)
        return category_created
    
    def get_category_by_name(self, name: str) -> CategoryModel:
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
        category_exists = self.__category_exists_by_name(name)
        if not category_exists:
            raise CategoryNotFound()
        category_founded = self.category_repository.get_category_by_name(name)
        category = CategoryModel(name=category_founded["name"]).model_dump_json()
        return category
    
    def get_category_by_id(self, category_id: str) -> CategoryModel:
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
        category_exists = self.__category_exists_by_id(category_id)
        if not category_exists:
            raise CategoryNotFound()
        category_founded = self.category_repository.get_category_by_id(category_id)
        category = CategoryModel(name=category_founded["name"]).model_dump_json()
        return category
    
    def get_all_categories(self) -> list:
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

    def update_category(self, category_id: str, name_category: str) -> str:
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
        category_exists = self.__category_exists_by_id(category_id)
        if not category_exists:
            raise CategoryNotFound()
        category_model_instance = CategoryModel(name=name_category)
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
        category_exists = self.__category_exists_by_id(category_id)
        if not category_exists:
            raise CategoryNotFound()
        category_deleted = self.category_repository.delete_category(category_id)
        return category_deleted
