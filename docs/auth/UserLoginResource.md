## Login
Allows users to use their registered details to log in to their account.

**URL**: localhost:[PORT]/users/api/v1/login

**Method**: `POST`

**Authentication**: Not required

## Request body
**Required fields:** `email`, `password`

**Optional fields:**

**Application data:**:
```bash
{
    "email": "Email from the user",
    "password": "Password from the user"
}
```

## Success response
**Code**: `200 OK`

**Content**:
```bash
{
    "message": "Login successful"
    "access_token": "8uP9dv0czfTLY8WEma1fZyBYLzUed.sXiwp31A4wQ6klpJclPYQyZDsFruLuybCsd..."
    "refresh_token": "8uP9dv0czfTLY8WEma1fZyBYLzUed.sXiwp31A4wQ6klpJclPYQyZDsFruLuybCd9..."
}
```

## Error response
**Condition**: If the entered `email` is not associated with a user account.

**Code**: `400 BAD REQUEST`

**Content**:
```bash
{
    "error": {
        "status": 400,
        "message": "User not found"
    }
}
```