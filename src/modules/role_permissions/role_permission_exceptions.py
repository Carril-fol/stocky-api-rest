class RolePermissionException(Exception):
    pass


class RolePermissionNotFound(RolePermissionException):

    def __init__(self, message="Not found Role Permission"):
        self.message = message
        super().__init__(self.message)


class RolePermissionsAlreadyHasAPermission(RolePermissionException):

    def __init__(self, message="The Role already has this permission"):
        self.message = message
        super().__init__(self.message)


class RoleNotInCompany(RolePermissionException):

    def __init__(self, message="Role does not belong to this company"):
        self.message = message
        super().__init__(self.message)