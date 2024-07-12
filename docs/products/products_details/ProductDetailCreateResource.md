## Create a detail of a product
Allows users to create products that are made up of a parent product

**URL**: localhost:[PORT]/product/detail/api/v1/create

**Method**: `POST`

**Authentication**: Required

## Request body
**Required fields:** `product_id`, `barcode`, `status`

**Application data:**:
```bash
{
    "product_id": "Id from product father",
    "barcode": "barcode from the product",
    "status": "Status from the product"
}
```

## Success response
**Code**: `201 CREATED`

**Content**:
```bash
{
    "msg": "Product detail created",
    "product detail": {
        "id": "Id from the product detail",
        "product_id": "Id from the product father",
        "barcode": "Barcode from the product detail",
        "status": "Status from the product"
    }
}
```

## Error response
**Condition**: If the product parent not exists.

**Code**: `400 BAD REQUEST`

**Content**:
```bash
{
    "error": "Product father no founded."
}
```