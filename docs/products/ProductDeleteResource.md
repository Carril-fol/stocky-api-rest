## Delete a product
Allows users to delete a product.

**URL**: localhost:[PORT]/product/api/v1/delete/<product_id>

**Method**: `DELETE`

**Authentication**: Required

## Success response
**Code**: `200 OK`

**Content**:
```bash
{
    "msg": "Product deleted"
}
```

## Error response
**Condition**: Missing ID in the URL

**Code**: `404 NOT FOUND`

**Content**:
```bash
{
    "error": "Missing ID in url."
}
```