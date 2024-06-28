import os
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()

class db:
  
    def __init__(self, dbURI = os.environ.get("MONGO_URI")):
        self.dbURI = dbURI
        self.client = MongoClient(self.dbURI)
        self.db = self.client["restful-inventory-manager"]
        self.usersCollections = self.db["user_accounts"]
        self.productsCollections = self.db["products"]

