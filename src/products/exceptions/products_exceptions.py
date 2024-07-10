class ProductException(Exception):
    pass


class NotExistingProductFather(ProductException):
    """
    """
    def __init__(self, message="Product father no founded"):
        self.message = message
        super().__init__(self.message)


class ExistingBarcodeException(ProductException):
    """
    Exception raised when a barcode already exists.
    """
    def __init__(self, message="Existing barcode"):
        self.message = message
        super().__init__(self.message)


class NotExistingBarcodeException(ProductException):
    """
    Exception raised when a barcode already exists.
    """
    def __init__(self, message="Not existing barcode"):
        self.message = message
        super().__init__(self.message)


class CannotCreateProductDetailsException(ProductException):
    """
    Exception raised when cannot create more product details.
    """
    def __init__(self, message="Cannot create more product details for this product"):
        self.message = message
        super().__init__(self.message)