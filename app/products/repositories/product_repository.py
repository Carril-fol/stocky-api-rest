from ..dao.product_dao import ProductDao
from ..domain.product_model import ProductModel

class ProductRepository:
    def __init__(self, product_dao: ProductDao):
        """
        Initializes the ProductRepository with a ProductDao instance.

        Args:
        product_dao (ProductDao): An instance of ProductDao which handles the database operations for products.
        """
        self.product_dao = product_dao

    def create_product(self, product_instance: ProductModel) -> ProductModel:
        """
        Creates a new product in the database and returns the created product instance.

        Args:
        product_instance (ProductModel): An instance of ProductModel containing the data for the new product.

        Returns:
        ProductModel: The created product instance with its data populated from the database.
        """
        return self.product_dao.create_product(product_instance)
    
    def get_product_by_id(self, product_id: str):
        """
        Retrieves a product from the database based on its unique identifier.

        Args:
        product_id (str): The unique identifier of the product to be retrieved.

        Returns:
        ProductModel: The retrieved product instance populated with data from the database.
                      Returns None if no product is found with the provided ID.
        """
        return self.product_dao.get_product_by_id(product_id)
    
    def update_product(self, product_id: str, product_instance: ProductModel) -> ProductModel:
        """
        Updates an existing product in the database and returns the updated product instance.

        Args:
        product_id (str): The unique identifier of the product to be updated.
        product_instance (ProductModel): An instance of ProductModel containing the new data for the product.

        Returns:
        ProductModel: The updated product instance populated with the new data.
                      Returns None if the product does not exist.
        """
        return self.product_dao.update_product(product_id, product_instance)
    
    def delete_product(self, product_id: str) -> ProductModel:
        """
        Deletes a product from the database based on its unique identifier and returns the deleted product instance.

        Args:
        product_id (str): The unique identifier of the product to be deleted.

        Returns:
        ProductModel: The deleted product instance populated with the data before deletion.
                      Returns None if no product is found with the provided ID.
        """
        return self.product_dao.delete_product(product_id)
