from bson import ObjectId
from products.repositories.product_detail_repository import ProductDetailRepository
from products.models.product_detail_model import ProductDetailModel
from products.services.product_service import ProductService
from products.exceptions.products_exceptions import *


class ProductDetailService:
    def __init__(self):
        self.product_detail_repository = ProductDetailRepository()
        self.product_service = ProductService()

    def __check_product_detail_exists_by_barcode(self, barcode: str) -> bool:
        """
        Checks if a product detail exists with a specific barcode.

        Parameters:
        ----------
        barcode (str): A barcode from a product

        Return:
        ------
        bool: Returns "True" if exists a product with a specific barcode and "False" if not
        """
        product_detail_instance = self.product_detail_repository.get_product_detail_by_barcode(barcode)
        return product_detail_instance if product_detail_instance else False
    
    def __can_create_product_details_from_father(self, product_id: str) -> bool:
        """
        Checks if can create product details from the product father.

        Parameters:
        ----------
        product_id (str): A product ID from the product father.

        Returns:
        -------
        bool: Returns "True" if the quantity found in a list is less than the quantity of the parent product, and "False" if not
        """
        product_father = self.product_service.get_product_by_id(product_id)
        if not product_father:
            raise NotExistingProductFather()
        products_details_from_father = self.product_detail_repository.get_products_details_by_product_id(product_id)
        products_details_list = [product_details for product_details in products_details_from_father]
        return True if product_father.quantity_product > len(products_details_list) else False

    def create_product_detail(self, product_id: str, barcode: str, status: str) -> ProductDetailModel:
        product_father_exists = self.product_service.get_product_by_id(product_id)
        if not product_father_exists:
            raise NotExistingProductFather()
        product_detail_exists = self.__check_product_detail_exists_by_barcode(barcode)
        if product_detail_exists:
            raise ExistingBarcodeException()
        can_create_product_details_from_father = self.__can_create_product_details_from_father(product_id)
        if not can_create_product_details_from_father:
            raise CannotCreateProductDetailsException()
        product_detail_model_instance = ProductDetailModel(
            product_id=ObjectId(product_id),
            barcode=barcode,
            status=status
        )
        product_create_instance = self.product_detail_repository.create_product_detail(product_detail_model_instance)
        return product_detail_model_instance
    
    def get_product_detail_by_barcode(self, barcode: str) -> ProductDetailModel:
        product_details_exists = self.__check_product_detail_exists_by_barcode(barcode)
        if not product_details_exists:
            raise NotExistingBarcodeException()
        product_details_model_instance = ProductDetailModel.model_validate(product_details_exists).model_dump_json()
        return product_details_model_instance
    
    def update_product_detail(self, barcode: str, status: str):
        product_details_exists = self.__check_product_detail_exists_by_barcode(barcode)
        if not product_details_exists:
            raise NotExistingBarcodeException()
        product_detail_new_model_instance = ProductDetailModel(status=status)
        product_detail_update = self.product_detail_repository.update_product_detail(barcode, product_detail_new_model_instance)
        return product_detail_update
    
    def delete_product_detail(self, barcode: str):
        product_details_exists = self.__check_product_detail_exists_by_barcode(barcode)
        if not product_details_exists:
            raise NotExistingBarcodeException()
        product_detail_delete = self.product_detail_repository.delete_product_detail(barcode)
        return product_detail_delete
