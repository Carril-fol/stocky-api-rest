from ..dao.product_detail_dao import ProductDetailDao

class ProductDetailRepository:
    def __init__(self):
        self.product_detail_dao = ProductDetailDao()

    def create_product_detail(self, product_detail_model_instance):
        return self.product_detail_dao.create_product_detail(product_detail_model_instance)
    
    def get_product_detail_by_barcode(self, barcode: str):
        return self.product_detail_dao.get_product_detail_by_barcode(barcode)
    
    def get_product_detail_by_id(self, id: str):
        return self.product_detail_dao.get_product_detail_by_id(id)
    
    def get_products_details_by_product_id(self, product_id: str):
        return self.product_detail_dao.get_products_details_by_product_id(product_id)
    
    def update_product_detail(self, barcode: str, product_detail_model_instance):
        return self.product_detail_dao.update_product_detail(barcode, product_detail_model_instance)
    
    def delete_product_detail(self, barcode: str):
        return self.product_detail_dao.delete_product_detail(barcode)