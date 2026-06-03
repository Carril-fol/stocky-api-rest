class RoleException(Exception):
    pass


class RoleNotFound(RoleException):

    def __init__(self, message = "Role not founded"):
        self.message = message
        super().__init__(self.message)


class RoleIsAlreadyInactive(RoleException):
    def __init__(self, message = "Role is already inactive"):
        self.message = message
        super().__init__(self.message)


class RoleIsAlreadyActive(RoleException):
    def __init__(self, message = "Role is already active"):
        self.message = message
        super().__init__(self.message)


class UserNotInCompany(RoleException):
    def __init__(self, message = "User does not belong to this company"):
        self.message = message
        super().__init__(self.message)


class RoleNameReserved(RoleException):
    def __init__(self, message = "Role name is reserved and cannot be used."):
        self.message = message
        super().__init__(self.message)