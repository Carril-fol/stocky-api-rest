from pymongo.results import InsertOneResult

from database.db import Database
from auth.models.token_model import TokenModel

class TokenDao(object):
    def __init__(self):
        """
        Initializes the TokenDao instance.

        Attributes:
        ----------
        database : Database
            An instance of the Database class, used to interact with the
            database.
            
        token_collection : Collection
            A reference to the collection in the database where user data
            is stored.
        """
        self.__database = Database()
        self.token_collection = self.__database.tokens_collection()

    def get_token_by_jti(self, token_jti: str):
        """
        Returns a instance from the token

        Args:
        ----
        token_jti (str): Is a unique identifier that contains the JWT tokens.

        Returns:
        -------
        dict: A dict with the all information from the database.
        """
        token = self.token_collection.find_one({"jti": token_jti})
        return token

    def blacklist_token(self, token_model_instance: TokenModel) -> InsertOneResult:
        """
        Inserts the token's data into the corresponding collection.

        Args:
        ----
        token_model_instance (TokenModel): Instance of the token model with 
        the data to be inserted.
        
        Returns:
        -------
        InsertOneResult: Insert result.
        """
        token_data_dict = token_model_instance.model_dump(by_alias=True)
        token_inserted = self.token_collection.insert_one(token_data_dict)
        return token_inserted