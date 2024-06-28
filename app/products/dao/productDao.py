from bson import ObjectId
from pymongo.results import DeleteResult, UpdateResult, InsertOneResult

from app.database.db import db
from app.products.domain.productModel import ProductModel

class ProductDAO:
    
    def __init__(self):
        self.productsCollections = db().productsCollections 

    def createProduct(self, productInstance: ProductModel) -> InsertOneResult:
        postDataDict = productInstance.dict(by_alias=True)
        result = self.productsCollections.insert_one(postDataDict)
        return result.inserted_id
    
    def getProductById(self, productId: str) -> ProductModel:
        result = self.productsCollections.find_one({"_id": ObjectId(productId)})
        return result
    
    def updateProduct(self, productId: str, productInstance: ProductModel) -> UpdateResult:
        productInstanceToUpdate = self.getProductById(productId)
        if not productInstanceToUpdate:
            return None
        
        productInstanceIdDict = {"_id": ObjectId(productId)}
        productNewDataDict = { 
            "$set": {
                "nameProduct": productInstance.nameProduct,
                "quantityProduct": productInstance.quantityProduct
            }
        }
        postUpdated = self.productsCollections.update_one(productInstanceIdDict, productNewDataDict)
        return postUpdated
    
    def deleteProduct(self, productId: str) -> DeleteResult:
        productInstanceIdDict = {"_id": ObjectId(productId)}
        productInstanceDelete = self.productsCollections.delete_one(productInstanceIdDict)
        return productInstanceDelete