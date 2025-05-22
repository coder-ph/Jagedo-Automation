# Jagedo API Documentation

## Table of Contents
1. [Authentication](#authentication)
2. [Users](#users)
3. [Projects](#projects)
4. [Bids](#bids)
5. [Documents](#documents)
6. [Payments](#payments)
7. [Notifications](#notifications)
8. [Places](#places)

## Authentication

### Register New User
```http
POST /api/auth/register
```

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "securepassword123",
  "role": "customer",
  "location": "Nairobi, Kenya"
}
```

### Login
```http
POST /api/auth/login
```

**Request Body:**
```json
{
  "email": "john@example.com",
  "password": "securepassword123"
}
```

### Get Current User Profile
```http
GET /api/auth/me
Authorization: Bearer <token>
```

## Users

### Get User Profile
```http
GET /api/profile
Authorization: Bearer <token>
```

### Update Profile
```http
PUT /api/profile
Authorization: Bearer <token>
```

## Projects

### Get All Projects
```http
GET /api/projects
```

**Query Parameters:**
- `status` - Filter by status (open, in_progress, completed)
- `category_id` - Filter by category
- `location` - Filter by location
- `page` - Page number (default: 1)
- `per_page` - Items per page (default: 10)

### Get Project by ID
```http
GET /api/projects/{project_id}
```

### Create Project
```http
POST /api/projects
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "title": "Website Development",
  "description": "Need a professional website",
  "category_id": 1,
  "location": "Nairobi",
  "budget": 50000
}
```

## Bids

### Submit Bid
```http
POST /api/bids
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "job_id": 1,
  "amount": 45000,
  "proposal": "I'll build your website with React and Node.js",
  "timeline_weeks": 4
}
```

### Get Bid by ID
```http
GET /api/bids/{bid_id}
Authorization: Bearer <token>
```

### Accept Bid
```http
POST /api/bids/{bid_id}/accept
Authorization: Bearer <token>
```

## Documents

### Upload Document
```http
POST /api/documents/upload
Content-Type: multipart/form-data
Authorization: Bearer <token>
```

**Form Data:**
- `file`: The file to upload
- `document_type`: Type of document (profile|bid|job|other)
- `job_id`: (Optional) Associated job ID
- `bid_id`: (Optional) Associated bid ID
- `title`: (Optional) Document title
- `description`: (Optional) Document description

### Download Document
```http
GET /api/documents/download/{attachment_id}
Authorization: Bearer <token>
```

### Delete Document
```http
DELETE /api/documents/{attachment_id}
Authorization: Bearer <token>
```

## Payments

### Initiate Payment
```http
POST /api/payments/initiate
Authorization: Bearer <token>
```

**Request Body:**
```json
{
  "job_id": 1,
  "amount": 50000,
  "phone": "254712345678"
}
```

### Check Payment Status
```http
GET /api/payments/status/{reference}
Authorization: Bearer <token>
```

## Notifications

### Get Notifications
```http
GET /api/notifications
Authorization: Bearer <token>
```

**Query Parameters:**
- `unread_only` - Show only unread notifications (true/false)
- `limit` - Number of notifications to return (default: 20)
- `offset` - Offset for pagination (default: 0)

### Mark Notification as Read
```http
POST /api/notifications/{notification_id}/read
Authorization: Bearer <token>
```

### Mark All Notifications as Read
```http
POST /api/notifications/read-all
Authorization: Bearer <token>
```

## Places

### Search Places
```http
GET /api/places/autocomplete?input=Nairobi
```

**Query Parameters:**
- `input` - Search query
- `location` - (Optional) Location bias "lat,lng"

### Get Place Details
```http
GET /api/places/details/{place_id}
```

## Error Responses

### Common Error Responses

**400 Bad Request**
```json
{
  "success": false,
  "error": "Error message"
}
```

**401 Unauthorized**
```json
{
  "success": false,
  "error": "Unauthorized"
}
```

**403 Forbidden**
```json
{
  "success": false,
  "error": "Insufficient permissions"
}
```

**404 Not Found**
```json
{
  "success": false,
  "error": "Resource not found"
}
```

**500 Internal Server Error**
```json
{
  "success": false,
  "error": "Internal server error"
}
```

## Rate Limiting
- All endpoints are rate limited to 1000 requests per hour per IP address
- Authentication endpoints have stricter rate limits (100 requests/hour/IP)

## Authentication
- All endpoints except `/api/auth/register` and `/api/auth/login` require authentication
- Include the JWT token in the `Authorization` header: `Bearer <token>`
- Tokens expire after 24 hours and can be refreshed using the refresh token

## Data Formats
- All dates are in ISO 8601 format: `YYYY-MM-DDTHH:MM:SSZ`
- All monetary amounts are in KES (Kenyan Shillings)
- File uploads are limited to 10MB per file
