## Update a product
Allows users to update the data from a product.

**URL**: localhost:[PORT]/product/api/v1/update/<product_id>

**Method**: `PUT`

**Authentication**: Required

## Request body
**Required fields:** `name_product`, `quantity_product`, `price`, `category_id`

**Application data:**:
```bash
{
    "name_product": "New name from product",
    "quantity_product": "New quantity from the product",
    "price": "New price from the product",
    "category_id": "New id from the category to the product".
}
```

## Success response
**Code**: `200 OK`

**Content**:
```bash
{
    "msg": "Product updated", 
    "product": {
        "name_product": "Name from product",
        "quantity_product": "Quantity from the product",
        "price": "Price from the product",
        "category_id": Id from the category to the product.
    }
}
```

## Error response
**Condition**: If the `product_id` entered not exists

**Code**: `400 BAD REQUEST`

**Content**:
```bash
{
    "error": "The entered product was not found"
}
```