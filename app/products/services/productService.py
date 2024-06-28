from app.products.repositories.productRepository import ProductRepository
from app.products.domain.productModel import ProductModel

class ProductService:
    
    def __init__(self, productRepository: ProductRepository):
        self.productRepository = productRepository

    def createProduct(self, nameProduct: str, quantityProduct: int) -> ProductModel:        
        productInstance = ProductModel(nameProduct=nameProduct, quantityProduct=quantityProduct)
        productCreated = self.productRepository.createProduct(productInstance)
        return productCreated
    
    def getProductById(self, productId: str) -> ProductModel:
        productInstance = self.productRepository.getProductById(productId)
        if not productInstance:
            return None
        
        productModelInstance = ProductModel(
            id=productInstance["_id"], 
            nameProduct=productInstance["nameProduct"], 
            quantityProduct=productInstance["quantityProduct"], 
        )
        return productModelInstance
    
    def updateProduct(self, productId: str, nameProduct: str, quantityProduct: int) -> ProductModel:
        productInstance = self.productRepository.getProductById(productId)
        if not productInstance:
            return None
        
        productInstance = ProductModel(nameProduct=nameProduct, quantityProduct=quantityProduct)
        productUpdate = self.productRepository.updateProduct(productId, productInstance)
        return productUpdate
    
    def deleteProduct(self, productId: str):
        productInstance = self.productRepository.getProductById(productId)
        if not productInstance:
            return None
        
        productDeleted = self.productRepository.deleteProduct(productId)
        return productDeleted