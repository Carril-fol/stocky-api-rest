from dotenv import load_dotenv
from pymongo import MongoClient
from settings import MONGO_URI
load_dotenv()

class Database(object):
    def __init__(self):
        self.__uri = MONGO_URI
        self.client = MongoClient(self.__uri)
        self.database = self.client["restful-inventory-manager"]

    def users_collection(self):
        """
        Return a instance from the users collection in the database
        """
        users_collection = self.database["users_accounts"]
        return users_collection
    
    def products_collection(self):
        """
        Return a instance from the product collection in the database
        """
        products_collection = self.database["products"]
        return products_collection

    def products_detail_collection(self):
        """
        Return a instance from the detail product collection in the database
        """
        products_detail_collection = self.database["detail_products"]
        return products_detail_collection

    def categories_collection(self):
        """
        Returns a instance from the categories collection in the database
        """
        categories_collection = self.database["categories"]
        return categories_collection
    
    def tokens_collection(self):
        tokens_blacklisted_colletions = self.database["tokens_blacklisted"]
        return tokens_blacklisted_colletions