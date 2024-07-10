from bson import ObjectId
from pymongo.results import InsertOneResult, UpdateResult

from auth.models.user_model import UserModel
from database.db import Database

class UserDao:
    def __init__(self):
        """
        Initializes the UserDao instance.

        Attributes:
        ----------
        database : Database
            An instance of the Database class, used to interact with the
            database.
            
        users_collections : Collection
            A reference to the collection in the database where user data
            is stored.
        """
        self.__database = Database()
        self.users_collections = self.__database.users_collection()

    def create_user(self, user_instance_model: UserModel) -> InsertOneResult:
        """
        Inserts the user's data into the corresponding collection and returns its ID.

        Args:
        ----
        user_instance_model_register (UserModelRegister): Instance of the user model with 
        the data to be inserted.
        
        Returns:
        -------
        InsertOneResult: Insert result, including the ID of the new document.
        """
        user_data_dict = user_instance_model.model_dump(by_alias=True)
        result = self.users_collections.insert_one(user_data_dict)
        return result.inserted_id
    
    def get_user_by_id(self, user_id: str) -> dict:
        """
        Returns a instance from the user

        Args:
        ----
        user_id (str): User ID to search

        Returns:
        -------
        UserModel: User model instance
        """
        user = self.users_collections.find_one({"_id": ObjectId(user_id)})
        return user if user else None
    
    def get_user_by_email(self, user_email: str) -> dict:
        """
        Return a instance from the user's

        Args:
        ----
        user_email (str): User email to search

        Returns:
        -------
        UserModel: user's information in model instance
        """
        user = self.users_collections.find_one({"email": user_email})
        return user if user else None
    
    def update_user(self, user_id: str, user_model_instance: UserModel) -> UpdateResult:
        """
        Return a instance the user updated

        Args:
        ----
        user_id (str): User id to search
        user_model_instance (UserModel): A UserModel with new information from the user

        Returns:
        -------
        UpdateResult: a instance from the user with the data updated 
        """
        user_id_dict = {
            "_id": ObjectId(user_id)
        }
        data_updated = user_model_instance.model_dump()
        user_instance_updated = self.users_collections.update_one(
            user_id_dict, 
            {"$set", data_updated}
        )
        return user_instance_updated