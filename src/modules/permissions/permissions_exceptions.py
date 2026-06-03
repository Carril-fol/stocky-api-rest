class PermissionException(Exception):
    pass


class PermissionNotFound(PermissionException):

    def __init__(self, message = "Permission does not found."):
        self.message = message
        super().__init__(self.message)


class PermissionAlreadyExists(PermissionException):

    def __init__(self, message = "Permission with that name already exists."):
        self.message = message
        super().__init__(self.message)


class InsufficientRolePrivileges(PermissionException):

    def __init__(self, message = "You don't have privileges for this action."):
        self.message = message
        super().__init__(self.message)