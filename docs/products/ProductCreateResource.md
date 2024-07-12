## Create a product
Allows users to register the data from a product.

**URL**: localhost:[PORT]/product/api/v1/create

**Method**: `POST`

**Authentication**: Required

## Request body
**Required fields:** `name_product`, `quantity_product`, `price`, `category_id`

**Application data:**:
```bash
{
    "name_product": "Name from product",
    "quantity_product": "Quantity from the product",
    "price": "Price from the product",
    "category_id": Id from the category to the product.
}
```

## Success response
**Code**: `201 CREATED`

**Content**:
```bash
{
    "msg": "Product created",
    "product": {
        "id": "Id from the product",
        "name_product": "Name from product",
        "quantity_product": "Quantity from the product",
        "price": "Price from the product",
        "category_id": "Id from the category to the product"
    }
}
```

## Error response
**Condition**: If the `quantity_product` is less than 0.

**Code**: `400 BAD REQUEST`

**Content**:
```bash
{
    "quantity_product": "The quantity of the product cannot be less than 0."
}
```