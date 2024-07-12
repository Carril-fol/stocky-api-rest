## Detail category
Allows users to see the details from a category.

**URL**: localhost:[PORT]/categories/api/v1/<name>

**Method**: `GET`

**Authentication**: Required

## URL Param
**Required fields:** `name`

## Success response
**Code**: `200 OK`

**Content**:
```bash
{
    "category": {
        "id": "Id from the category",
        "name": "Name from the category"
    }
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