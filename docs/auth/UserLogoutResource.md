## Logout
Allows users to logout from their accounts.

**URL**: localhost:[PORT]/users/api/v1/logout

**Method**: `POST`

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
    "msg": "Logout succesfully"
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