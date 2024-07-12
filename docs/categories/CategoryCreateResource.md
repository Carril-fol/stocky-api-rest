## Create category
Allows users to create categories for their products.

**URL**: localhost:[PORT]/categories/api/v1/create

**Method**: `POST`

**Authentication**: Required

## Request body
**Required fields:** `name`

**Application data:**:
```bash
{
    "name": "Name from the category"
}
```

## Success response
**Code**: `201 CREATED`

**Content**:
```bash
{
    "msg": "Category created",
    "category": {
        "id": "Id from the category",
        "name": "Name from the category"
    }
}
```

## Error response
**Condition**: If category already exists.

**Code**: `400 BAD REQUEST`

**Content**:
```bash
{
    "error": "Category already exists"
}
```