# Jagedo API Documentation

## Table of Contents
1. [Authentication](#authentication)
2. [Projects](#projects)
3. [Bids](#bids)
4. [Payments](#payments)
5. [Notifications](#notifications)
6. [Documents](#documents)

## Authentication

### Register a New User
- **Endpoint**: `POST /auth/register`
- **Description**: Register a new user account
- **Request Body**:
  ```json
  {
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "role": "customer",
    "location": "Nairobi, Kenya"
  }
  ```
- **Response**:
  ```json
  {
    "status": "success",
    "message": "User registered successfully",
    "data": {
      "user_id": 1,
      "email": "john@example.com",
      "role": "customer"
    }
  }
  ```

### Login
- **Endpoint**: `POST /auth/login`
- **Description**: Authenticate user and get access tokens
- **Request Body**:
  ```json
  {
    "email": "john@example.com",
    "password": "securepassword123"
  }
  ```
- **Response**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```

### Refresh Token
- **Endpoint**: `POST /auth/refresh`
- **Description**: Get a new access token using refresh token
- **Headers**:
  - `Authorization: Bearer <refresh_token>`
- **Response**:
  ```json
  {
    "access_token": "new_access_token_here"
  }
  ```

### Get Current User Profile
- **Endpoint**: `GET /auth/me`
- **Description**: Get current authenticated user's profile
- **Headers**:
  - `Authorization: Bearer <access_token>`
- **Response**:
  ```json
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "customer",
    "location": "Nairobi, Kenya"
  }
  ```

## Projects

### Create Project
- **Endpoint**: `POST /projects`
- **Description**: Create a new project
- **Headers**:
  - `Authorization: Bearer <access_token>`
  - `Content-Type: multipart/form-data`
- **Form Data**:
  - `title`: Project title (required)
  - `description`: Project description (required)
  - `category_id`: Category ID (required)
  - `location`: Project location (required)
  - `budget`: Project budget (required)
  - `timeline_weeks`: Estimated timeline in weeks (optional)
  - `documents[]`: Project documents (optional, multiple files)
- **Response**:
  ```json
  {
    "id": 1,
    "title": "Website Development",
    "description": "Need a professional website",
    "status": "open",
    "budget": 50000,
    "created_at": "2023-05-22T10:00:00Z"
  }
  ```

### Get All Projects
- **Endpoint**: `GET /projects`
- **Description**: Get all projects with optional filters
- **Query Parameters**:
  - `status`: Filter by status (open, in_progress, completed, cancelled)
  - `category_id`: Filter by category ID
  - `min_budget`: Minimum budget
  - `max_budget`: Maximum budget
  - `location`: Filter by location
  - `page`: Page number (default: 1)
  - `per_page`: Items per page (default: 10)
- **Response**:
  ```json
  {
    "projects": [...],
    "total": 15,
    "page": 1,
    "per_page": 10,
    "total_pages": 2
  }
  ```

### Get Project by ID
- **Endpoint**: `GET /projects/<int:project_id>`
- **Description**: Get project details by ID
- **Response**:
  ```json
  {
    "id": 1,
    "title": "Website Development",
    "description": "Need a professional website",
    "status": "open",
    "budget": 50000,
    "created_at": "2023-05-22T10:00:00Z",
    "bids_count": 5,
    "documents": [...]
  }
  ```

## Bids

### Submit Bid
- **Endpoint**: `POST /bids`
- **Description**: Submit a bid for a project
- **Headers**:
  - `Authorization: Bearer <access_token>`
  - `Content-Type: multipart/form-data`
- **Form Data**:
  - `job_id`: Project ID (required)
  - `amount`: Bid amount (required)
  - `proposal`: Detailed proposal (required)
  - `timeline_weeks`: Estimated timeline in weeks (required)
  - `documents[]`: Supporting documents (optional, multiple files)
- **Response**:
  ```json
  {
    "id": 1,
    "job_id": 1,
    "professional_id": 2,
    "amount": 45000,
    "status": "submitted",
    "created_at": "2023-05-22T11:00:00Z"
  }
  ```

### Get Bid Details
- **Endpoint**: `GET /bids/<int:bid_id>`
- **Description**: Get bid details by ID
- **Headers**:
  - `Authorization: Bearer <access_token>`
- **Response**:
  ```json
  {
    "id": 1,
    "job_id": 1,
    "professional": {
      "id": 2,
      "name": "Jane Smith",
      "rating": 4.8
    },
    "amount": 45000,
    "proposal": "Detailed proposal text...",
    "status": "submitted",
    "documents": [...]
  }
  ```

### Accept Bid
- **Endpoint**: `POST /bids/<int:bid_id>/accept`
- **Description**: Accept a bid and award the project
- **Headers**:
  - `Authorization: Bearer <access_token>`
- **Response**:
  ```json
  {
    "success": true,
    "message": "Bid accepted successfully",
    "project": {
      "id": 1,
      "status": "in_progress",
      "assigned_to": 2
    }
  }
  ```

## Payments

### Initiate M-Pesa Payment
- **Endpoint**: `POST /payments/initiate/mpesa`
- **Description**: Initiate M-Pesa payment
- **Headers**:
  - `Authorization: Bearer <access_token>`
- **Request Body**:
  ```json
  {
    "phone": "254712345678",
    "amount": 1000,
    "project_id": 1,
    "description": "Project deposit"
  }
  ```
- **Response**:
  ```json
  {
    "success": true,
    "message": "Payment initiated",
    "transaction_id": "MP-12345678"
  }
  ```

### Get Payment Transactions
- **Endpoint**: `GET /payments/transactions`
- **Description**: Get user's payment transactions
- **Query Parameters**:
  - `status`: Filter by status (pending, completed, failed, cancelled)
  - `method`: Filter by payment method (mpesa, card, bank_transfer)
  - `project_id`: Filter by project ID
  - `page`: Page number (default: 1)
  - `limit`: Items per page (default: 10)
- **Response**:
  ```json
  {
    "transactions": [...],
    "total": 5,
    "page": 1,
    "per_page": 10
  }
  ```

## Notifications

### Get Notifications
- **Endpoint**: `GET /notifications`
- **Description**: Get user's notifications
- **Query Parameters**:
  - `unread_only`: Return only unread notifications (true/false)
  - `limit`: Number of notifications to return (default: 20)
  - `offset`: Offset for pagination (default: 0)
  - `mark_read`: Mark notifications as read when fetched (true/false)
- **Response**:
  ```json
  {
    "notifications": [
      {
        "id": 1,
        "title": "New Bid Received",
        "message": "You have received a new bid for your project",
        "read": false,
        "created_at": "2023-05-22T12:00:00Z",
        "type": "bid_received"
      }
    ],
    "total": 3,
    "unread_count": 1
  }
  ```

### Mark Notification as Read
- **Endpoint**: `PUT /notifications/<int:notification_id>/read`
- **Description**: Mark a notification as read
- **Response**:
  ```json
  {
    "success": true,
    "message": "Notification marked as read"
  }
  ```

## Documents

### Upload Document
- **Endpoint**: `POST /documents/upload`
- **Description**: Upload a document
- **Headers**:
  - `Authorization: Bearer <access_token>`
  - `Content-Type: multipart/form-data`
- **Form Data**:
  - `file`: The file to upload (required)
  - `document_type`: Type of document (profile, bid, project)
  - `job_id`: Required if document_type is project
  - `bid_id`: Required if document_type is bid
- **Response**:
  ```json
  {
    "id": 1,
    "filename": "proposal.pdf",
    "url": "/documents/download/1",
    "size": 1024,
    "mimetype": "application/pdf"
  }
  ```

### Download Document
- **Endpoint**: `GET /documents/download/<int:document_id>`
- **Description**: Download a document by ID
- **Response**: File download

## Error Responses

### 400 Bad Request
```json
{
  "status": "error",
  "message": "Validation failed",
  "errors": {
    "email": "Invalid email format",
    "password": "Password must be at least 8 characters"
  }
}
```

### 401 Unauthorized
```json
{
  "status": "error",
  "message": "Authentication required"
}
```

### 403 Forbidden
```json
{
  "status": "error",
  "message": "Insufficient permissions"
}
```

### 404 Not Found
```json
{
  "status": "error",
  "message": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "status": "error",
  "message": "An unexpected error occurred"
}
```

## Rate Limiting
- All endpoints are rate limited to 100 requests per minute per IP address.
- Authentication endpoints have a lower limit of 10 requests per minute.

## Authentication
- All endpoints except `/auth/register` and `/auth/login` require authentication.
- Include the JWT token in the `Authorization` header:
  ```
  Authorization: Bearer <your_jwt_token>
  ```

## Pagination
- List endpoints support pagination using `page` and `per_page` query parameters.
- The response includes pagination metadata:
  ```json
  {
    "data": [...],
    "total": 100,
    "page": 1,
    "per_page": 10,
    "total_pages": 10
  }
  ```

## Sorting
- List endpoints support sorting using the `sort` query parameter:
  - `sort=field` for ascending order
  - `sort=-field` for descending order
  - Example: `?sort=-created_at` for newest first
