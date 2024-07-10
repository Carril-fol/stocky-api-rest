from pymongo.results import InsertOneResult, UpdateResult
from auth.dao.user_dao import UserDao
from auth.models.user_model import UserModel

class UserRepository:
    def __init__(self):
        """
        Initializes the UserRepository instance.

        Attributes:
        ----------
        user_dao : UserDao
            An instance of the UserDao class, used to interact with the
            database.
        """
        self.user_dao = UserDao()

    def create_user(self, user_instance_model: UserModel) -> InsertOneResult:
        """
        Inserts the user's data into the corresponding collection and returns its ID.

        Args:
        ----
        user_data (UserModel): Instance from the model

        Returns:
        -------
        UserModel: Insert result, including the ID of the new document.
        """
        user_created = self.user_dao.create_user(user_instance_model)
        return user_created

    def get_user_by_id(self, user_id: str) -> dict:
        """
        Returns a instance from the user

        Args:
        user_id (str): User ID to search

        Returns:
        UserModel: User model instance
        """
        return self.user_dao.get_user_by_id(user_id)
    
    def get_user_by_email(self, user_email: str) -> dict:
        """
        Return a instance from the user's

        Args:
        user_email (str): User email to search

        Returns:
        UserModel: user's information in model instance
        """
        return self.user_dao.get_user_by_email(user_email)

    def update_user(self, user_id: str, user_model_instance: UserModel) -> UpdateResult:
        """  
        Replaces new information in a record where it matches the ID entered.

        Args:
        ----
        user_id (str): ID from the user.
        user_model_instance (UserModel): Instance from the model

        Returns:
        -------
        UpdateResult: a instance from the user with the data updated
        """
        return self.user_dao.update_user(user_id, user_model_instance)