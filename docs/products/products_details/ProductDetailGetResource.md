## Get detail of a product detail
Returns product details information

**URL**: localhost:[PORT]/product/detail/api/v1/<barcode>

**Method**: `POST`

**Authentication**: Required

## Success response
**Code**: `200 OK`

**Content**:
```bash
{
    "product": {
        "id": "Id from the product detail",
        "product_id": "Id from the product father",
        "barcode": "Barcode from the product detail",
        "status": "Status from the product"
    }
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