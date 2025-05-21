# Jagedo API Documentation

## Base URL
`http://your-domain.com/api`

## Authentication
Most endpoints require authentication using JWT tokens. Include the token in the `Authorization` header:
```
Authorization: Bearer <your_jwt_token>
```

## Table of Contents
1. [Authentication](#authentication)
2. [Users](#users)
3. [Projects](#projects)
4. [Bids](#bids)
5. [Documents](#documents)
6. [Places API](#places-api)

---

## Authentication

### Login
```http
POST /api/login
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

---

## Users

### Get User Profile
```http
GET /api/profile
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Profile retrieved successfully",
  "data": {
    "id": 1,
    "email": "user@example.com",
    "name": "John Doe",
    "role": "customer",
    "location": "Nairobi, Kenya",
    "company_name": "ACME Corp",
    "profile_description": "Professional contractor"
  }
}
```

---

## Projects

### Create Project
```http
POST /api/projects
```

**Request Body (multipart/form-data):**
- `title` (string, required)
- `description` (string, required)
- `budget` (number, required)
- `location` (string, required)
- `category_id` (integer, required)
- `files[]` (array of files, optional)

**Success Response (201 Created):**
```json
{
  "success": true,
  "message": "Project created successfully",
  "data": {
    "project_id": 1,
    "file_count": 2
  }
}
```

### Get Project Details
```http
GET /api/projects/{project_id}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "data": {
    "id": 1,
    "title": "Website Development",
    "description": "Need a responsive website",
    "status": "open",
    "budget": 1000.00,
    "location": "Nairobi, Kenya",
    "created_at": "2025-05-21T10:00:00Z"
  }
}
```

### List Project Documents
```http
GET /api/projects/{project_id}/documents
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "documents": [
    {
      "id": 1,
      "filename": "requirements.pdf",
      "file_type": "application/pdf",
      "size": 1024,
      "is_owner": true,
      "file_url": "/api/documents/1"
    }
  ]
}
```

---

## Bids

### Submit Bid
```http
POST /api/projects/{project_id}/bids
```

**Request Body:**
```json
{
  "amount": 800.00,
  "proposal": "I can complete this project within 2 weeks",
  "timeline_weeks": 2
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Bid submitted successfully",
  "data": {
    "bid_id": 1,
    "project_id": 1,
    "amount": 800.00,
    "status": "pending"
  }
}
```

### Get Project Bids
```http
GET /api/projects/{project_id}/bids
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "bids": [
    {
      "id": 1,
      "amount": 800.00,
      "proposal": "I can complete this project within 2 weeks",
      "status": "pending",
      "professional": {
        "id": 2,
        "name": "Jane Smith",
        "company_name": "Web Pros",
        "rating": 4.8
      }
    }
  ]
}
```

### Select Winning Bid
```http
POST /api/projects/{project_id}/select-winner
```

**Request Body:**
```json
{
  "bid_id": 1
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Winning bid selected successfully",
  "data": {
    "bid_id": 1,
    "contractor_id": 2,
    "score": 95.5
  }
}
```

---

## Documents

### Download Document
```http
GET /api/documents/{document_id}
```

**Success Response:**
- Returns the file as an attachment

### Delete Document
```http
DELETE /api/documents/{document_id}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Document deleted successfully"
}
```

---

## Places API

### Place Autocomplete
```http
GET /api/places/autocomplete?query=Nairobi
```

**Query Parameters:**
- `query` (string, required): Search query
- `location` (string, optional): "lat,lng" for biasing results
- `radius` (number, optional): Search radius in meters (default: 50000)
- `language` (string, optional): Language code (default: 'en')

**Success Response (200 OK):**
```json
{
  "status": "success",
  "predictions": [
    {
      "description": "Nairobi, Kenya",
      "place_id": "ChIJd8BlQ2BZwokRAFUEcm_qrcA",
      "types": ["locality", "political", "geocode"],
      "structured_formatting": {
        "main_text": "Nairobi",
        "secondary_text": "Kenya"
      }
    }
  ]
}
```

### Place Details
```http
GET /api/places/details/{place_id}
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "result": {
    "formatted_address": "Nairobi, Kenya",
    "geometry": {
      "location": {
        "lat": -1.2920659,
        "lng": 36.8219462
      },
      "viewport": {
        "northeast": {
          "lat": -1.219766870107278,
          "lng": 36.91522587989272
        },
        "southwest": {
          "lat": -1.352083129892722,
          "lng": 36.65066852010728
        }
      }
    },
    "place_id": "ChIJd8BlQ2BZwokRAFUEcm_qrcA",
    "types": ["locality", "political"]
  }
}
```

## Error Responses

### 400 Bad Request
```json
{
  "success": false,
  "message": "Validation error",
  "errors": {
    "field_name": ["Error message"]
  }
}
```

### 401 Unauthorized
```json
{
  "success": false,
  "message": "Authentication required"
}
```

### 403 Forbidden
```json
{
  "success": false,
  "message": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "success": false,
  "message": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "success": false,
  "message": "An unexpected error occurred"
}
```

## Rate Limiting
- All API endpoints are rate limited to 1000 requests per hour per IP address.
- The following headers are included in rate-limited responses:
  - `X-RateLimit-Limit`: The maximum number of requests allowed in the time window
  - `X-RateLimit-Remaining`: The number of requests remaining in the current window
  - `X-RateLimit-Reset`: The time at which the current rate limit window resets (UTC epoch seconds)

## Versioning
- The current API version is `v1`.
- Include the version in the `Accept` header:
  ```
  Accept: application/vnd.jagedo.v1+json
  ```

## Changelog

### v1.0.0 (2025-05-21)
- Initial API release
- Added Projects, Bids, and Documents endpoints
- Integrated Google Places API for location services
