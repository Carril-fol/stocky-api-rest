from bson import ObjectId
from pymongo.results import DeleteResult, UpdateResult, InsertOneResult

from database.db import Database
from products.models.product_model import ProductModel

class ProductDao:
    def __init__(self):
        self.database = Database()
        self.products_collection = self.database.products_collection()

    def create_product(self, product_instance: ProductModel) -> InsertOneResult:
        """
        Inserts the product's data into the corresponding collection and returns its ID.

        Args:
        ----
        product_instance (ProductModel):

        Returns:
        -------
        The id of the product inserted in the collection
        """
        product_data_dict = product_instance.model_dump(by_alias=True)
        result = self.products_collection.insert_one(product_data_dict)
        return result.inserted_id
    
    def get_product_by_id(self, product_id: str):
        """
        Returns a instance from the product's

        Args:
        ----
        product_id (str): Product id to search

        Returns:
        -------
        UserModel: User model instance
        """
        result = self.products_collection.find_one({ "_id": ObjectId(product_id)})
        return result
    
    def update_product(self, product_id: str, product_instance: ProductModel) -> UpdateResult:
        """
        Updates an existing product in the database with new data and returns the result of the update operation.

        Args:
        ----
        product_id (str): The unique identifier of the product to be updated.
        product_instance (ProductModel): An instance of ProductModel containing the new data for the product.

        Returns:
        -------
        UpdateResult: An instance of UpdateResult containing information about the update operation, 
                    such as the number of documents matched and modified. Returns None if the product does not exist.
        """
        product_instance_id_dict = {
            "_id": ObjectId(product_id)
        }
        product_new_data_dict = { 
            "$set": {
                "name_product": product_instance.name_product,
                "quantity_product": product_instance.quantity_product,
                "price": product_instance.price,
                "category_id": product_instance.category_id
            }
        }
        product_updated = self.products_collection.update_one(product_instance_id_dict, product_new_data_dict)
        return product_updated
    
    def delete_product(self, product_id: str) -> DeleteResult:
        """
        Deletes a product from the database based on its unique identifier.

        Args:
        ----
        productId (str): The unique identifier of the product to be deleted.

        Returns:
        -------
        DeleteResult: An instance of DeleteResult containing information about the delete operation,
                    such as the number of documents deleted. If no product is found with the provided ID,
                    the number of documents deleted will be 0.
        """
        product_instance_id_dict = {
            "_id": ObjectId(product_id)
        }
        product_instance_delete = self.products_collection.delete_one(product_instance_id_dict)
        return product_instance_delete