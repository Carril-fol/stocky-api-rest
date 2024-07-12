## Delete category
Allows users to delete the category.

**URL**: localhost:[PORT]/categories/api/v1/delete/<category_id>

**Method**: `GET`

**Authentication**: Required

## URL Param
**Required fields:** `category_id`

## Success response
**Code**: `200 OK`

**Content**:
```bash
{
    "category": "deleted"
}
```

## Error response
**Condition**: If category not exists.

**Code**: `400 BAD REQUEST`

**Content**:
```bash
{
    "error": "Category does not exists"
}
```