from pymongo.results import InsertOneResult

from auth.dao.token_dao import TokenDao
from auth.models.token_model import TokenModel

class TokenRepository(object):
    def __init__(self):
        """
        Initializes the TokenRepository instance.

        Attributes:
        ----------
        token_dao : TokenDao
            An instance of the TokenDao class, used to interact with the
            database.
        """
        self.token_dao = TokenDao()

    def get_token_by_jti(self, token_jti: str):
        """
        Returns a dict from the token

        Args:
        ----
        token_jti (str): JTI from the token

        Returns:
        -------
        dict: A dict with the information from the token
        """
        return self.token_dao.get_token_by_jti(token_jti)
    
    def blacklist_token(self, token_model_instance: TokenModel) -> InsertOneResult:
        """
        Inserts the token´s data into the corresponding collection.

        Args:
        ----
        token_model_instance (TokenModel): Instance of the token model with 
        the data to be inserted.
        
        Returns:
        -------
        InsertOneResult: Insert result.
        """
        return self.token_dao.blacklist_token(token_model_instance)