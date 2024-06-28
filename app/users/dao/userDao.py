from bson import ObjectId
from pymongo.results import InsertOneResult

from ...database.db import db
from ..domain.userModel import UserModel

class UserDAO:
    
    def __init__(self):
        self.usersCollections = db().usersCollections

    def createUser(self, userData: UserModel) -> InsertOneResult:
        userDataDict = userData.dict(by_alias=True)
        result = self.usersCollections.insert_one(userDataDict)
        return result.inserted_id
    
    def getUserById(self, userId: str) -> UserModel:
        user = self.usersCollections.find_one(
            {"_id": ObjectId(userId)}
        )
        return user if user else None
    
    def getUserByEmail(self, userEmail: str) -> UserModel:
        user = self.usersCollections.find_one(
            {"email": userEmail}
        )
        return user if user else None
    
    def updateUser(self, userId: str, dataUpdated: dict) -> UserModel:
        userInstance = self.getUserById(userId)
        if userInstance:
            userUpdated = self.usersCollections.update_one(
                {"_id": ObjectId(userInstance.id)}, 
                {"$set", dataUpdated}
            )
            return userUpdated
        return None