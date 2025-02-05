class StockException(Exception):
    pass


class StockNotFound(StockException):
    def __init__(self, message="Stock not found."):
        self.message = message
        super().__init__(self.message)


class StockHasAlreadyStatus(StockException):

    def __init__(self, message="The entered stock already has the status"):
        self.message = message
        super().__init__(self.message)