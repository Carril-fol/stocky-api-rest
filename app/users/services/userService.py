from werkzeug.security import generate_password_hash, check_password_hash

from ..repositories.userRepository import UserRepository
from ..domain.userModel import UserModel

class UserService:
  
    def __init__(self, userRepository: UserRepository):
        self.userRepository = userRepository

    def _hashPassword(self, password: str):
        return generate_password_hash(password)

    def _verifyPassword(self, password: str, passwordHashed: str):
        return check_password_hash(passwordHashed, password)

    def getUserById(self, userId: str):
        userInstance = self.userRepository.getUserById(userId)
        if not userInstance:
            return None
        
        userModelInstance = UserModel(
            id=userInstance["_id"],
            firstName=userInstance["firstName"],
            lastName=userInstance["lastName"],
            email=userInstance["email"],
            password=userInstance["password"],
            isAuthenticated=userInstance["isAuthenticated"],
            isAdmin=userInstance["isAdmin"],
            isSuperUser=userInstance["isSuperUser"]
        )
        return userModelInstance
    
    def getUserByEmail(self, userEmail: str):
        userInstance = self.userRepository.getUserByEmail(userEmail)
        if not userInstance:
            return None
        
        userModelInstance = UserModel(
            id=userInstance["_id"],
            firstName=userInstance["firstName"],
            lastName=userInstance["lastName"],
            email=userInstance["email"],
            password=userInstance["password"],
            isAuthenticated=userInstance["isAuthenticated"],
            isAdmin=userInstance["isAdmin"],
            isSuperUser=userInstance["isSuperUser"]
        )
        return userModelInstance

    def createUser(self, firstName: str, lastName: str, email: str, password: str) -> UserModel:
        existingUser = self.userRepository.getUserByEmail(email)
        if existingUser:
            raise ValueError("Email already registered")
        
        passwordHashed = self._hashPassword(password)
        userData = UserModel(firstName=firstName, lastName=lastName, email=email, password=passwordHashed)
        userCreated = self.userRepository.createUser(userData)
        return userCreated

    def authenticationUser(self, email: str, password: str):
        existingUser = self.getUserByEmail(email)
        passwordUserStored = existingUser.password
        if existingUser and self._verifyPassword(password, passwordUserStored):
            return existingUser
        return None