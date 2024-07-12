## Detail a product
Allows users to view product details.

**URL**: localhost:[PORT]/product/api/v1/detail/<product_id>

**Method**: `GET`

**Authentication**: Required

## Success response
**Code**: `201 CREATED`

**Content**:
```bash
{
    "product": {
        "id": "Id from the product
        "name_product": "Name from the product",
        "quantity_product": "Quantity from the product",
        "price": "Price from the product",
        "category_id": "Category ID from the product"
    }
}
```

## Error response
**Condition**: If the product don`t exists

**Code**: `404 NOT FOUND`

**Content**:
```bash
{
    "error": "The entered product was not found."
}
```