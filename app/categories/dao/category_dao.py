from bson import ObjectId
from pymongo.results import DeleteResult, UpdateResult, InsertOneResult

from app.database.db import Database
from ..domain.category_model import CategoryModel

class CategoryDao:
    def __init__(self):
        self.database = Database()
        self.category_collection = self.database.categories_collection()

    def create_category(self, category_model_instance: CategoryModel) -> InsertOneResult:
        """
        Inserts the product's data into the corresponding collection and returns its ID.

        Args:
        category_model_instance (CategoryModel): 

        Returns:
        The id of the product inserted in the collection
        """
        category_data_dict = category_model_instance.dict(by_alias=True)
        category_inserted = self.category_collection.insert_one(category_data_dict)
        return category_inserted.inserted_id
    
    def get_category_by_name(self, name: str):
        """
        Returns a dict from the category selected

        Args:
        name (str): The name of the category to be filtered.

        Returns:
        dict: a dictionary with the category data
        """
        found_category = self.category_collection.find_one({"name": name})
        return found_category
    
    def get_category_by_id(self, category_id: str):
        """
        Returns a dict from the category selected

        Args:
        category_id (str): The ID of the category to be filtered.

        Returns:
        dict: a dictionary with the category data
        """
        category_found = self.category_collection.find_one({ "_id": ObjectId(category_id)})
        return category_found
    
    def get_all_categories(self) -> list:
        """
        Returns a list with all categories in the collection

        Returns:
        list: a list with all categories
        """
        categories = self.category_collection.find()
        return categories
    
    def update_category(self, category_id: str, category_instance: CategoryModel) -> UpdateResult:
        """
        Updates a category in the database with new data provied

        Args:
        ----
        category_id (str): The ID of the category to be updated.
                        
        category_instance (CategoryModel): An instance of the `CategoryModel` 
        containing the new category data.
        In this case, only the `name` field is updated.

        Returns:
        -------
        UpdateResult: An `UpdateResult` object containing information about the update operation.
        """
        category_found = self.get_category_by_id(category_id)
        if not category_found:
            return None
        
        category_dict_id = {"_id": ObjectId(category_id)}
        category_new_data_dict = { 
            "$set": {
                "name": category_instance.name,
            }
        }
        category_updated = self.category_collection.update_one(category_dict_id, category_new_data_dict)
        return category_updated

    def delete_category(self, category_id: str) -> DeleteResult:
        """
        Deletes a category in they respective collection in database

        Args:
        ----
        category_id (str): The ID of the category to be deleted.

        Returns:
        -------
        DeleteResult: An `DeleteResult` object containing information about the delete operation.
        """
        category_dict_with_id = {"_id": ObjectId(category_id)}
        category_instance_delete = self.category_collection.delete_one(category_dict_with_id)
        return category_instance_delete