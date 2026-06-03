class CompanyException(Exception):
    pass


class CompanyNotFound(CompanyException):

    def __init__(self, message = "Company does not found."):
        self.message = message
        super().__init__(self.message)