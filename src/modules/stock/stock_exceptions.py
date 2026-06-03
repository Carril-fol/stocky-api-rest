class StockException(Exception):
    pass


class StockNotFound(StockException):
    def __init__(self, message="Stock not found."):
        self.message = message
        super().__init__(self.message)