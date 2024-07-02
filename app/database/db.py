from dotenv import load_dotenv
from pymongo import MongoClient
from ..settings import MONGO_URI
load_dotenv()

class Database:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.database = self.client["restful-inventory-manager"]

    def users_collection(self):
        """
        Return a instance from the users collection in the database
        """
        users_collection = self.database["user_accounts"]
        return users_collection
    
    def products_collection(self):
        """
        Return a instance from the product collection in the database
        """
        products_collection = self.database["products"]
        return products_collection

    def products_detail_collection(self):
        products_detail_collection = self.database["detail_products"]
        return products_detail_collection

    def categories_collection(self):
        categories_collection = self.database["categories"]
        return categories_collection
