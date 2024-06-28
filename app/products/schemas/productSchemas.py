from marshmallow import Schema, fields, validate, validates, ValidationError

class ProductSchema(Schema):
    nameProduct = fields.String(
        required=True, 
        validate=validate.Length(min=3, max=160)
    )
    quantityProduct = fields.Integer(
        required=True
    )
    
    @validates("nameProduct")
    def validateNameProduct(self, nameProduct: str):
        if len(nameProduct) < 3:
            raise ValidationError("Please enter a name that is more than 0 characters.")
        
    @validates("quantityProduct")
    def validateCantProduct(self, cantProduct: int):
        if cantProduct < 0:
            raise ValidationError("The quantity of the product cannot be less than 0.")