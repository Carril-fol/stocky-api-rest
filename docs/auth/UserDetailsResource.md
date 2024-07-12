## User Detail
Allows users to see their information.

**URL**: localhost:[PORT]/users/api/v1/<user_id>

**Method**: `GET`

**Authentication**: Required

**Header Authorization:**:
```bash
{
    Authorization: "8uP9dv0czfTLY8WEma1fZyBYLzUedsX.iwp31A4wQ6klpJclPYQyZDsFruLuybCd9..."
}
```

## Success response
**Code**: `200 OK`

**Content**:
```bash
{
    "user": {
        "id": "Id from the user",
        "first_name": "First name from the user",
        "last_name": "Last name from the user",
        "email": "Email from the user",
        "password": "Password from the user"
    }
}
```

## Error response
**Condition**: Missing Authorization Header.

**Code**: `400 BAD REQUEST`

**Content**:
```bash
{
    "msg": "Missing Authorization Header"
}
```