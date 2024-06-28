from app.products.dao.productDao import ProductDAO
from app.products.domain.productModel import ProductModel

class ProductRepository:
  
    def __init__(self, productDao: ProductDAO):
        self.productDao = productDao

    def createProduct(self, productInstance: ProductModel) -> ProductModel:
        return self.productDao.createProduct(productInstance)
    
    def getProductById(self, productId: str) -> ProductModel:
        return self.productDao.getProductById(productId)
    
    def updateProduct(self, productId: str, productInstance: ProductModel) -> ProductModel:
        return self.productDao.updateProduct(productId, productInstance)
    
    def deleteProduct(self, productId: str) -> ProductModel:
        return self.productDao.deleteProduct(productId)    