from werkzeug.security import generate_password_hash, check_password_hash
from ..repositories.user_repository import UserRepository
from ..domain.user_model import UserModelRegister, UserModel

class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def __hash_password(self, password: str) -> str:
        """
        Generates a hashed password using the scrypt algorithm.
        
        Args:
        password (str): Plain text password to be hashed.
        
        Returns:
        str: The hashed password.
        """
        return generate_password_hash(password)

    def __verify_password(self, password_hashed: str, password: str) -> bool:
        """
        Verifies if the provided password matches the hashed password.
        
        Args:
        password (str): Plain text password to verify.
        password_hashed (str): Hashed password to compare against.
        
        Returns:
        bool: True if the password matches, False otherwise.
        """
        return check_password_hash(password_hashed, password)

    def get_user_by_id(self, user_id: str) -> UserModel:
        """
        Retrieves a user by their ID and returns a UserModel instance with their details.
        
        Args:
        user_id (str): The ID of the user to retrieve.
        
        Returns:
        UserModel: Instance with the user's details, or None if the user is not found.
        """
        user_instance = self.user_repository.get_user_by_id(user_id)
        if not user_instance:
            raise Exception("User not found")
  
        user_model_instance = UserModel(
            id=user_instance["_id"],
            first_name=user_instance["first_name"],
            last_name=user_instance["last_name"],
            email=user_instance["email"],
            password=user_instance["password"],
            is_authenticated=user_instance["is_authenticated"],
            is_admin=user_instance["is_admin"],
            is_superuser=user_instance["is_superuser"]
        )
        return user_model_instance

    def get_user_by_email(self, user_email: str) -> UserModel:
        """
        Retrieves a user by their email and returns a UserModel instance with their details.
        
        Args:
        user_email (str): The email of the user to retrieve.
        
        Returns:
        UserModel: Instance with the user's details, or None if the user is not found.
        """
        user_instance = self.user_repository.get_user_by_email(user_email)
        if not user_instance:
            raise Exception("User not found")
        
        user_model_instance = UserModel(
            id=user_instance["_id"],
            first_name=user_instance["first_name"],
            last_name=user_instance["last_name"],
            email=user_instance["email"],
            password=user_instance["password"],
            is_authenticated=user_instance["is_authenticated"],
            is_admin=user_instance["is_admin"],
            is_superuser=user_instance["is_superuser"]
        )
        return user_model_instance

    def create_user(self, first_name: str, last_name: str, email: str, password: str, confirm_password: str) -> UserModel:
        """
        Creates a new user with the provided details, ensuring the email is not already registered.
        
        Args:
        ----
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        email (str): The email address of the user.
        password (str): The plain text password of the user.
        confirm_password (str): The plain text password of the user. 
        
        Returns:
        -------
        UserModelRegister: Instance of the newly created user.
        
        Raises:
        ValueError: If the email is already registered.
        """
        existing_user = self.user_repository.get_user_by_email(email)
        if existing_user:
            raise Exception("Email already registered")
        
        user_instance_model_register = UserModelRegister(
            first_name=first_name, 
            last_name=last_name, 
            email=email, 
            password=password,
            confirm_password=confirm_password
        )
        
        password_hashed = self.__hash_password(user_instance_model_register.confirm_password)
        passwords_check_hashed = self.__verify_password(password_hashed, confirm_password)
        if not passwords_check_hashed:
            raise Exception("Password don't match.")
        
        user_instance_model = UserModel(
            first_name=user_instance_model_register.first_name, 
            last_name=user_instance_model_register.last_name, 
            email=user_instance_model_register.email, 
            password=password_hashed,
        )
        user_created = self.user_repository.create_user(user_instance_model)
        return user_created

    def authenticate_user(self, email: str, password: str) -> UserModel:
        """
        Authenticates a user by their email and password.
        
        Args:
        ----
        email (str): The email of the user attempting to authenticate.
        password (str): The plain text password provided by the user.
        
        Returns:
        -------
        UserModel: The authenticated user instance if credentials are valid, None otherwise.
        """
        user_instance = self.get_user_by_email(email)
        if not user_instance:
            return None
        
        password_user_stored = user_instance.password
        if self.__verify_password(password_user_stored, password):
            return user_instance
        return None
