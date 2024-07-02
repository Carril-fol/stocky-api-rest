from ..dao.user_dao import UserDAO
from ..domain.user_model import UserModel

class UserRepository:
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao

    def create_user(self, user_instance_model: UserModel) -> UserModel:
        """
        Inserts the user's data into the corresponding collection and returns its ID.

        Args:
        user_data (UserModel): Instance from the model

        Returns:
        UserModel: Insert result, including the ID of the new document.
        """
        user_created = self.user_dao.create_user(user_instance_model)
        return user_created

    def get_user_by_id(self, user_id: str) -> UserModel:
        """
        Returns a instance from the user

        Args:
        user_id (str): User ID to search

        Returns:
        UserModel: User model instance
        """
        return self.user_dao.get_user_by_id(user_id)
    
    def get_user_by_email(self, user_email: str) -> UserModel:
        """
        Return a instance from the user's

        Args:
        user_email (str): User email to search

        Returns:
        UserModel: user's information in model instance
        """
        return self.user_dao.get_user_by_email(user_email)