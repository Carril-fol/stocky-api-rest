class SupplierException(Exception):
    pass


class SupplierNotFound(SupplierException):
    def __init__(self, message="Supplier not found."):
        self.message = message
        super().__init__(self.message)


class SupplierAlreadyExists(SupplierException):
    def __init__(self, message="Supplier with that name already exists."):
        self.message = message
        super().__init__(self.message)


class SupplierHasAlreadyStatus(SupplierException):
    def __init__(self, message="Status from the supplier is already that status."):
        self.message = message
        super().__init__(self.message)