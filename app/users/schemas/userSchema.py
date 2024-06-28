from marshmallow import Schema, fields, validate, validates, ValidationError

class UserRegisterSchema(Schema):
    firstName = fields.String(
        required=True, 
        validate=validate.Length(min=3, max=20)
    )
    lastName = fields.String(
        required=True, 
        validate=validate.Length(min=3, max=20)
    )
    email = fields.Email(
        required=True, 
        validate=validate.Length(min=1, max=120)
    )
    password = fields.String(
        required=True, 
        validate=validate.Length(min=6, max=30)
    )
    confirmPassword = fields.String(
        required=True, 
        validate=validate.Length(min=6, max=30)
    )

    @validates("password")
    def validatePasswordDigistAndLetter(self, password):
        if not any(str(char).isdigit() for char in password):
            raise ValidationError("Password must contain at least one number.")
        if not any(str(char).isalpha() for char in password):
            raise ValidationError("Password must contain at least one letter.")
        return password
        
    @validates("confirmPassword")
    def validateConfirmpassword(self, confirmPassword):
        if not any(str(char).isdigit() for char in confirmPassword):
            raise ValidationError("Password must contain at least one number.")
        if not any(str(char).isalpha() for char in confirmPassword):
            raise ValidationError("Password must contain at least one letter.")

    @validates("email")
    def validateEmailAddresses(self, email):
        emailAddresses = ["gmail.com", "hotmail.com"]
        emailSplit = (str(email)).split("@")
        if not emailSplit[1] in emailAddresses:
            raise ValidationError("The email provider is not allowed.")


class UserLoginSchema(Schema):
    email = fields.Email(
        required=True, 
        validate=validate.Length(min=1, max=120)
    )
    password = fields.String(
        required=True, 
        validate=validate.Length(min=6, max=30)
    )

    @validates("password")
    def validatePasswordDigistAndLetter(self, password):
        if not any(str(char).isdigit() for char in password):
            raise ValidationError("Password must contain at least one number.")
        if not any(str(char).isalpha() for char in password):
            raise ValidationError("Password must contain at least one letter.")
        return password

    @validates("email")
    def validateEmailAddresses(self, email):
        emailAddresses = ["gmail.com", "hotmail.com", "yahoo.com"]
        emailSplit = (str(email)).split("@")
        if not emailSplit[1] in emailAddresses:
            raise ValidationError("The email provider is not allowed.")
        return email