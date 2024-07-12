## Detail all categories
Allows users to see the all categories.

**URL**: localhost:[PORT]/categories/api/v1/all

**Method**: `GET`

**Authentication**: Required

## Success response
**Code**: `200 OK`

**Content**:
```bash
{
    "categories": [
        {
            "id": "Id from the category",
            "name": "Name from the category"
        },
        ...
    ]
}
```