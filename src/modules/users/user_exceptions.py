class UserException(Exception):
    pass


class UserNotFound(UserException):

    def __init__(self, message = "Invalid credentials."):
        self.message = message
        super().__init__(self.message)


class EmailInvalidFormat(UserException):

    def __init__(self, message = "The email format is invalid."):
        self.message = message
        super().__init__(self.message)


class UserWithAnEmailAlreadyExists(UserException):

    def __init__(self, message = "A User with that email already exists."):
        self.message = message
        super().__init__(self.message)


class PasswordDontMatch(UserException):

    def __init__(self, message = "Invalid credentials."):
        self.message = message
        super().__init__(self.message)
