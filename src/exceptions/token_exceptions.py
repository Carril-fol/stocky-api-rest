class TokenException(Exception):
    pass


class TokenAlreadyBlacklisted(TokenException):
    def __init__(self, message = "The entered user token is already on the blacklist"):
        self.message = message
        super().__init__(self.message)