from ..dao.userDao import UserDAO
from ..domain.userModel import UserModel

class UserRepository:
    
    def __init__(self, userDao: UserDAO):
        self.userDao = userDao

    def createUser(self, userData: UserModel) -> UserModel:
        return self.userDao.createUser(userData)
    
    def getUserById(self, userId: str):
        return self.userDao.getUserById(userId)
    
    def getUserByEmail(self, userEmail: str) -> UserModel:
        return self.userDao.getUserByEmail(userEmail)