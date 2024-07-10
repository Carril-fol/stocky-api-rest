from bson import ObjectId

from products.repositories.product_repository import ProductRepository
from products.models.product_model import ProductModel
from categories.services.category_service import CategoryService

class ProductService:
    def __init__(self):
        """
        Initializes the ProductService with a ProductRepository instance.

        Args:
        ----
        product_repository (ProductRepository): An instance of ProductRepository which handles the operations for products.
        category_service (CategoryService): An instance of CategoryService which handles the operations for categories.
        """
        self.product_repository = ProductRepository()
        self.category_service = CategoryService()

    def create_product(self, name_product: str, quantity_product: int, price: int, category_id: str) -> ProductModel:
        """
        Creates a new product in the database and returns the created product instance.

        Args:
        ----
        name_product (str): The name of the product to be created.
        quantity_product (int): The quantity of the product to be created.
        price (int): The price of the product to be created.
        category_id (str): The category ID of the product to be created.

        Returns:
        -------
        ProductModel: The created product instance with its data populated from the database.
        """
        category_found = self.category_service.get_category_by_id(category_id)
        if not category_found:
            raise Exception("Category not founded")
        product_model_instance = ProductModel(
            name_product=name_product,
            quantity_product=quantity_product,
            price=price,
            category_id=ObjectId(category_id)
        )
        product_created = self.product_repository.create_product(product_model_instance)
        return product_created

    def get_product_by_id(self, product_id: str) -> ProductModel:
        """
        Retrieves a product from the database based on its unique identifier and returns it as a ProductModel instance.

        Args:
        product_id (str): The unique identifier of the product to be retrieved.

        Returns:
        ProductModel: The retrieved product instance populated with data from the database.
                    Returns None if no product is found with the provided ID.
        """
        product_instance = self.product_repository.get_product_by_id(product_id)
        if not product_instance:
            raise Exception("The entered product was not found")
        product_model_instance = ProductModel(
            id=product_instance["_id"],
            name_product=product_instance["name_product"], 
            quantity_product=product_instance["quantity_product"],
            price=product_instance["price"],
            category_id=product_instance["category_id"]
        ).model_dump_json()
        return product_model_instance

    def update_product(self, product_id: str, name_product: str, quantity_product: int, price: int, category_id: str) -> ProductModel:
        """
        Updates an existing product in the database and returns the updated product instance.

        Args:
        product_id (str): The unique identifier of the product to be updated.
        name_product (str): The new name of the product.
        quantity_product (int): The new quantity of the product.

        Returns:
        ProductModel: The updated product instance populated with the new data.
                    Returns None if the product does not exist.
        """
        product_instance = self.product_repository.get_product_by_id(product_id)
        if not product_instance:
            raise Exception("The entered product was not found")
        product_model_instance = ProductModel(
            name_product=name_product, 
            quantity_product=quantity_product, 
            price=price, 
            category_id=ObjectId(category_id)
        )
        product_update = self.product_repository.update_product(product_id, product_model_instance)
        return product_update

    def delete_product(self, product_id: str):
        """
        Deletes a product from the database based on its unique identifier.

        Args:
        product_id (str): The unique identifier of the product to be deleted.

        Returns:
        ProductModel: The deleted product instance populated with the data before deletion.
                    Returns None if no product is found with the provided ID.
        """
        product_instance = self.product_repository.get_product_by_id(product_id)
        if not product_instance:
            raise Exception("The entered product was not found")   
        product_deleted = self.product_repository.delete_product(product_id)
        return product_deleted
