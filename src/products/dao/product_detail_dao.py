from bson import ObjectId
from pymongo.results import InsertOneResult

from database.db import Database
from products.models.product_detail_model import ProductDetailModel

class ProductDetailDao:
    def __init__(self):
        self.database = Database()
        self.product_detail_collection = self.database.products_detail_collection()

    def create_product_detail(self, product_detail_model_instance: ProductDetailModel) -> InsertOneResult:
        product_detail_data_dict = product_detail_model_instance.model_dump(by_alias=True)
        product_detail_inserted = self.product_detail_collection.insert_one(product_detail_data_dict)
        return product_detail_inserted

    def get_product_detail_by_barcode(self, barcode: str):
        product_detail_instance = self.product_detail_collection.find_one({"barcode": barcode})
        return product_detail_instance
    
    def get_products_details_by_product_id(self, product_id: str):
        products_details_instance = self.product_detail_collection.find({"product_id": ObjectId(product_id)})
        return products_details_instance
    
    def get_product_detail_by_id(self, id: str):
        product_detail_instance = self.product_detail_collection.find_one({"_id": ObjectId(id)})
        return product_detail_instance

    def update_product_detail(self, id: str, product_detail_model_instance: ProductDetailModel):
        product_detail_id_dict = {
            "_id": ObjectId(id)
        }
        product_detail_new_data_dict = { 
            "$set": {
                "product_id": product_detail_model_instance.product_id,
                "barcode": product_detail_model_instance.barcode,
                "status": product_detail_model_instance.status,
            }
        }
        product_detail_update_instance = self.product_detail_collection.update_one(product_detail_id_dict, product_detail_new_data_dict)
        return product_detail_update_instance
    
    def delete_product_detail(self, barcode: str):
        product_detail_delete_data_dict = {
            "barcode": barcode
        }
        product_detail_delete_instance = self.product_detail_collection.delete_one(product_detail_delete_data_dict)
        return product_detail_delete_instance