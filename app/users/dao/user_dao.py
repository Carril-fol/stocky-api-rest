from bson import ObjectId
from pymongo.results import InsertOneResult

from ...database.db import Database
from ..domain.user_model import UserModel, UserModelRegister

class UserDAO:
    def __init__(self):
        self.users_collections = Database().users_collection()

    def create_user(self, user_instance_model: UserModel) -> InsertOneResult:
        """
        Inserts the user's data into the corresponding collection and returns its ID.

        Args:
        ----
        user_instance_model_register (UserModelRegister): Instance of the user model with the data to be inserted.
        
        Returns:
        -------
        InsertOneResult: Insert result, including the ID of the new document.
        """
        user_data_dict = user_instance_model.dict(by_alias=True)
        result = self.users_collections.insert_one(user_data_dict)
        return result.inserted_id
    
    def get_user_by_id(self, user_id: str) -> UserModel:
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
    
    def get_user_by_email(self, user_email: str) -> UserModel:
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
    
    def update_user(self, user_id: str, data_updated: dict) -> UserModel:
        """
        Return a instance the user updated

        Args:
        ----
        user_id (str): User id to search
        data_updated (dict): Dict with new information from the user

        Returns:
        -------
        UserMode: a instance from the user with the data updated 
        """
        user_instance = self.get_user_by_id(user_id)
        if not user_instance:
            return None
        user_updated = self.users_collections.update_one(
                {"_id": ObjectId(user_instance.id)}, 
                {"$set", data_updated}
            )
        return user_updated
