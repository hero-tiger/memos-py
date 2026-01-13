# API Documentation

## Overview

Memos Python API provides a RESTful interface for managing users, memos, attachments, and more. The API is documented using OpenAPI 3.0 specification and is available at:

- **Swagger UI**: http://localhost:8081/api/docs
- **ReDoc**: http://localhost:8081/api/redoc
- **OpenAPI JSON**: http://localhost:8081/api/openapi.json

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the `Authorization` header:

```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Getting an Access Token

1. **Sign Up**
```http
POST /api/v1/auth/signup
Content-Type: application/json

{
  "username": "testuser",
  "email": "test@example.com",
  "password": "password123"
}
```

2. **Sign In**
```http
POST /api/v1/auth/signin?email=test@example.com&password=password123
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

## API Endpoints

### Authentication

#### Sign Up
```http
POST /api/v1/auth/signup
```

Creates a new user account.

**Request Body:**
```json
{
  "username": "string (3-100 chars)",
  "email": "string (valid email)",
  "password": "string (min 6 chars)",
  "nickname": "string (optional)",
  "avatar_url": "string (optional)",
  "description": "string (optional)"
}
```

**Response:** `UserResponse`

#### Sign In
```http
POST /api/v1/auth/signin
```

Authenticates a user and returns an access token.

**Query Parameters:**
- `email`: User's email
- `password`: User's password

**Response:** `Token`

### Users

#### Get Current User
```http
GET /api/v1/users/me
```

Returns the currently authenticated user's information.

**Authentication:** Required

**Response:** `UserResponse`

#### Update Current User
```http
PATCH /api/v1/users/me
```

Updates the currently authenticated user's profile.

**Authentication:** Required

**Request Body:**
```json
{
  "nickname": "string (optional)",
  "avatar_url": "string (optional)",
  "description": "string (optional)"
}
```

**Response:** `UserResponse`

#### List Users
```http
GET /api/v1/users?skip=0&limit=100
```

Returns a list of users.

**Authentication:** Required

**Query Parameters:**
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100)

**Response:** `List[UserResponse]`

#### Get User by ID
```http
GET /api/v1/users/{user_id}
```

Returns a specific user by ID.

**Authentication:** Required

**Path Parameters:**
- `user_id`: User ID

**Response:** `UserResponse`

### Memos

#### Create Memo
```http
POST /api/v1/memos
```

Creates a new memo.

**Authentication:** Required

**Request Body:**
```json
{
  "content": "string (markdown supported)",
  "visibility": "PUBLIC|PROTECTED|PRIVATE",
  "tags": ["string"],
  "pinned": false
}
```

**Response:** `MemoResponse`

#### List Memos
```http
GET /api/v1/memos?creator_id=1&visibility=PRIVATE&tag=test&pinned=true&skip=0&limit=100
```

Returns a list of memos with optional filters.

**Query Parameters:**
- `creator_id`: Filter by creator ID (optional)
- `visibility`: Filter by visibility (optional)
- `tag`: Filter by tag (optional)
- `pinned`: Filter by pinned status (optional)
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100)

**Response:** `List[MemoResponse]`

#### Get Memo by ID
```http
GET /api/v1/memos/{memo_id}
```

Returns a specific memo by ID.

**Path Parameters:**
- `memo_id`: Memo ID

**Response:** `MemoResponse`

#### Get Memo by UID
```http
GET /api/v1/memos/uid/{uid}
```

Returns a specific memo by UID.

**Path Parameters:**
- `uid`: Memo UID

**Response:** `MemoResponse`

#### Update Memo
```http
PATCH /api/v1/memos/{memo_id}
```

Updates a specific memo.

**Authentication:** Required

**Path Parameters:**
- `memo_id`: Memo ID

**Request Body:**
```json
{
  "content": "string (optional)",
  "visibility": "PUBLIC|PROTECTED|PRIVATE (optional)",
  "tags": ["string"] (optional),
  "pinned": false (optional)
}
```

**Response:** `MemoResponse`

#### Delete Memo
```http
DELETE /api/v1/memos/{memo_id}
```

Deletes a specific memo.

**Authentication:** Required

**Path Parameters:**
- `memo_id`: Memo ID

**Response:** `204 No Content`

### Attachments

#### Upload Attachment
```http
POST /api/v1/attachments
```

Uploads a file attachment.

**Authentication:** Required

**Request Body:** `multipart/form-data`
- `file`: File to upload (required)
- `memo_id`: Associated memo ID (optional)

**Response:** `AttachmentResponse`

#### List Attachments
```http
GET /api/v1/attachments?memo_id=1&skip=0&limit=100
```

Returns a list of attachments.

**Authentication:** Required

**Query Parameters:**
- `memo_id`: Filter by memo ID (optional)
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100)

**Response:** `List[AttachmentResponse]`

#### Get Attachment
```http
GET /api/v1/attachments/{attachment_id}
```

Returns a specific attachment.

**Authentication:** Required

**Path Parameters:**
- `attachment_id`: Attachment ID

**Response:** `AttachmentResponse`

#### Delete Attachment
```http
DELETE /api/v1/attachments/{attachment_id}
```

Deletes a specific attachment.

**Authentication:** Required

**Path Parameters:**
- `attachment_id`: Attachment ID

**Response:** `204 No Content`

### Personal Access Tokens

#### Create PAT
```http
POST /api/v1/tokens
```

Creates a new Personal Access Token.

**Authentication:** Required

**Request Body:**
```json
{
  "description": "string (optional)",
  "expires_in_days": 30 (optional)
}
```

**Response:** `PersonalAccessTokenResponse`

#### List PATs
```http
GET /api/v1/tokens
```

Returns a list of user's Personal Access Tokens.

**Authentication:** Required

**Response:** `List[PersonalAccessTokenResponse]`

#### Delete PAT
```http
DELETE /api/v1/tokens/{token_id}
```

Deletes a specific Personal Access Token.

**Authentication:** Required

**Path Parameters:**
- `token_id`: Token ID

**Response:** `204 No Content`

### Search

#### Search Memos
```http
GET /api/v1/search/memos?query=search-term&creator_id=1&visibility=PRIVATE&tag=test&skip=0&limit=100
```

Searches memos by content.

**Query Parameters:**
- `query`: Search query (required)
- `creator_id`: Filter by creator ID (optional)
- `visibility`: Filter by visibility (optional)
- `tag`: Filter by tag (optional)
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100)

**Response:** `List[MemoResponse]`

#### Filter Memos
```http
GET /api/v1/filter/memos?creator_id=1&visibility=PRIVATE&tag=test&pinned=true&content_contains=text&date_from=2024-01-01&date_to=2024-12-31&skip=0&limit=100
```

Filters memos with multiple criteria.

**Query Parameters:**
- `creator_id`: Filter by creator ID (optional)
- `visibility`: Filter by visibility (optional)
- `tag`: Filter by tag (optional)
- `pinned`: Filter by pinned status (optional)
- `content_contains`: Filter by content (optional)
- `date_from`: Filter by date from (ISO format, optional)
- `date_to`: Filter by date to (ISO format, optional)
- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100)

**Response:** `List[MemoResponse]`

#### Get Tags
```http
GET /api/v1/tags?creator_id=1
```

Returns all unique tags.

**Query Parameters:**
- `creator_id`: Filter by creator ID (optional)

**Response:**
```json
{
  "tags": ["tag1", "tag2", "tag3"]
}
```

#### Get Stats
```http
GET /api/v1/stats?creator_id=1
```

Returns memo statistics.

**Query Parameters:**
- `creator_id`: Filter by creator ID (optional)

**Response:**
```json
{
  "total_memos": 100,
  "pinned_memos": 10,
  "visibility_counts": {
    "PUBLIC": 20,
    "PROTECTED": 30,
    "PRIVATE": 50
  },
  "total_tags": 15,
  "unique_tags": ["tag1", "tag2", "tag3"]
}
```

## Data Models

### UserResponse
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "nickname": "Test User",
  "avatar_url": "https://example.com/avatar.jpg",
  "role": "USER",
  "description": "User description",
  "created_ts": "2024-01-01T00:00:00Z",
  "updated_ts": "2024-01-01T00:00:00Z"
}
```

### MemoResponse
```json
{
  "id": 1,
  "uid": "550e8400-e29b-41d4-a716-446655440000",
  "creator_id": 1,
  "creator": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com"
  },
  "content": "# Hello World\n\nThis is a memo.",
  "visibility": "PRIVATE",
  "tags": ["test", "hello"],
  "pinned": false,
  "created_ts": "2024-01-01T00:00:00Z",
  "updated_ts": "2024-01-01T00:00:00Z"
}
```

### AttachmentResponse
```json
{
  "id": 1,
  "uid": "550e8400-e29b-41d4-a716-446655440000",
  "creator_id": 1,
  "memo_id": 1,
  "filename": "document.pdf",
  "file_type": "application/pdf",
  "file_size": 1024,
  "storage_type": "local",
  "reference": "/path/to/file.pdf",
  "created_ts": "2024-01-01T00:00:00Z"
}
```

## Error Responses

The API uses standard HTTP status codes and returns error details in the response body:

```json
{
  "detail": "Error message"
}
```

Common status codes:
- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `204 No Content`: Request successful, no content returned
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Access denied
- `404 Not Found`: Resource not found
- `422 Unprocessable Entity`: Validation error
- `500 Internal Server Error`: Server error

## Rate Limiting

Currently, there is no rate limiting implemented. Consider implementing rate limiting for production use.

## Pagination

Most list endpoints support pagination using `skip` and `limit` query parameters:

- `skip`: Number of records to skip (default: 0)
- `limit`: Maximum number of records to return (default: 100, max: 100)

## Visibility Levels

Memos support three visibility levels:

- **PUBLIC**: Visible to everyone
- **PROTECTED**: Visible only to authenticated users
- **PRIVATE**: Visible only to the creator

## Markdown Support

Memos support Markdown formatting. The following features are available:

- Headers (#, ##, ###)
- Bold (**text**)
- Italic (*text*)
- Links ([text](url))
- Images (![alt](url))
- Code blocks (```code```)
- Lists (- item)
- Task lists (- [ ] item)
- Tables
- Blockquotes
- Front matter

## Examples

### Complete Workflow

1. **Sign Up**
```bash
curl -X POST http://localhost:8081/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "securepassword"
  }'
```

2. **Sign In**
```bash
curl -X POST "http://localhost:8081/api/v1/auth/signin?email=john@example.com&password=securepassword"
```

3. **Create a Memo**
```bash
curl -X POST http://localhost:8081/api/v1/memos \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "# My First Memo\n\nThis is a **bold** statement.",
    "visibility": "PRIVATE",
    "tags": ["first", "test"]
  }'
```

4. **Search Memos**
```bash
curl -X GET "http://localhost:8081/api/v1/search/memos?query=bold" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

5. **Upload Attachment**
```bash
curl -X POST http://localhost:8081/api/v1/attachments \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@document.pdf" \
  -F "memo_id=1"
```

## Support

For issues and questions, please refer to the main [README.md](README.md) or open an issue on GitHub.
