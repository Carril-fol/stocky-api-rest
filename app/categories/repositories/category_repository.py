from ..dao.category_dao import CategoryDao
from ..domain.category_model import CategoryModel

class CategoryRepository:
    def __init__(self, category_dao: CategoryDao):
        self.category_dao = category_dao

    def create_category(self, category_model_instance: CategoryModel):
        """
        Creates a new category in their respective collection in the database

        Args:
        ----
        category_model_instance (CategoryModel): An instance of "CategoryModel" containing the category data.

        Returns:
        -------
        dict: The newly created category data from the database, typically including an `id`.
        """
        return self.category_dao.create_category(category_model_instance)
    
    def get_category_by_name(self, name: str):
        """
        Retrieve a category by its name.

        Args:
        ----
        name (str): The name of the category to retrieve.

        Returns:
        -------
        dict: The category data if found, or `None` if no category with the given name exists.
        """
        return self.category_dao.get_category_by_name(name)

    def get_category_by_id(self, category_id: str):
        """
        Retrieve a category by its ID.

        Args:
        ----
        category_id (str): The ID of the category to retrieve.

        Returns:
        -------
        dict: The category data if found, or `None` if no category with the given ID exists.
        """
        return self.category_dao.get_category_by_id(category_id)

    def get_categories(self) -> list:
        """
        Retrieve all categories from the database.

        Returns:
        -------
        list: A list of dictionaries, each representing a category.
        """
        return self.category_dao.get_all_categories()
    
    def update_category(self, category_id: str, category_instance: CategoryModel):
        """
        Update an existing category in the database.

        Args:
        ----
        category_id (str): The ID of the category to update.
        category_instance (CategoryModel): An instance of `CategoryModel` containing the updated data.

        Returns:
        -------
        UpdateResult: An `UpdateResult` object with information about the update operation.
        """
        return self.category_dao.update_category(category_id, category_instance)
    
    def delete_category(self, category_id: str):
        """
        Delete a category from the database by its ID.

        Args:
        ----
        category_id (str): The ID of the category to delete.

        Returns:
        -------
        DeleteResult: A `DeleteResult` object with information about the deletion operation.
        """
        return self.category_dao.delete_category(category_id)