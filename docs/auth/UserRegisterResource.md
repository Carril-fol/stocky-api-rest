## Register
Allows users to register their data.

**URL**: localhost:[PORT]/users/api/v1/register

**Method**: `POST`

**Authentication**: Not required

## Request body
**Required fields:** `first_name`, `last_name`, `email`, `password`, `confirm_password`

**Optional fields:**

**Application data:**:
```bash
{
    "first_name": "First name from the user",
    "last_name": "Last name from the user",
    "email": "Email from the user",
    "password": "Password from the user",
    "confirm_password": "Confirmation password from the user"
}
```

## Success response
**Code**: `201 Created`

**Content**:
```bash
{
    "msg": "User created",
    "user": {
        "id": "Id from the user",
        "first_name": "First name from the user",
        "last_name": "Last name from the user",
        "email": "Email from the user",
        "password": "Password from the user",
        "confirm_password": "Confirmation from the password"
    },
    "access_token": "8uP9dv0czfTLY8WEma1fZyBYLzUedsXiwp31A4wQ6klpJclPYQyZDsFruLuybCd9..."
}
```

## Error response
**Condition**: If already `email` exists.

**Code**: `400 Bad Request`

**Content**:
```bash
{
    "error": {
        "status": 400,
        "message": "User already exists"
    }
}
```