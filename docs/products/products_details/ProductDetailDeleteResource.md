## Delete a detail from a product.
Allows users to delete details of a parent product.

**URL**: localhost:[PORT]/product/detail/delete/api/v1/<barcode>

**Method**: `DELETE`

**Authentication**: Required

## Success response
**Code**: `200 OK`

**Content**:
```bash
{
    "product": "Deleted"
}
```

## Error response
**Condition**: If the product parent no exists.

**Code**: `400 BAD REQUEST`

**Content**:
```bash
{
    "error": "Product parent no founded."
}
```