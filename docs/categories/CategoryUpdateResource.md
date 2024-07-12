## Update category
Allows users to see the details from a category.

**URL**: localhost:[PORT]/categories/api/v1/update/<category_id>

**Method**: `PUT`

**Authentication**: Required

## Request body
**Required fields:** `name`

**Application data:**:
```bash
{
    "name": "New name for the category"
}
```

## Success response
**Code**: `200 OK`

**Content**:
```bash
{
    "category updated": {
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
    "error": "Category does not found."
}
```