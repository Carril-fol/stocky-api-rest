class ProductException(Exception):
    pass


class ProductNotFound(ProductException):

    def __init__(self, message="The entered product was not found"):
        self.message = message
        super().__init__(self.message)


class ProductHasAlreadyStatus(ProductException):

    def __init__(self, message="The entered product already has the status"):
        self.message = message
        super().__init__(self.message)