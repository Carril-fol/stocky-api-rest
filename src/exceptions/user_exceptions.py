class UserException(Exception):
    pass


class UserNotFoundException(UserException):
    def __init__(self, message = "User not founded"):
        self.message = message
        super().__init__(self.message)


class UserAlreadyExists(UserException):
    def __init__(self, message = "User already exists"):
        self.message = message
        super().__init__(self.message)


class PasswordDontMatch(UserException):
    def __init__(self, message = "Passwords don't match"):
        self.message = message
        super().__init__(self.message)


class PasswordDontContainSpecialCharecters(UserException):
    def __init__(self, message = "Password must contain at least one special character."):
        self.message = message
        super().__init__(self.message)