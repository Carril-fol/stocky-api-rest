class CategoryException(Exception):
    pass


class CategoryNotFound(CategoryException):

    def __init__(self, message = "Category does not found."):
        self.message = message
        super().__init__(self.message)


class CategoryAlreadyExists(CategoryException):

    def __init__(self, message = "Category already exists."):
        self.message = message
        super().__init__(self.message)


class CategoryStatusError(CategoryException):
    
    def __init__(self, message = "Category already has status."):
        self.message = message
        super().__init__(self.message)