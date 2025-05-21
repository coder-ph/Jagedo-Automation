# Jagedo API - Quick Reference

## Base URL
`https://api.jagedo.com/v1`

## Authentication
```
POST /auth/register
POST /auth/login
POST /auth/refresh
GET  /auth/me
```

## Projects
```
GET    /projects           # List projects
POST   /projects           # Create project
GET    /projects/{id}      # Get project details
PUT    /projects/{id}      # Update project
GET    /projects/{id}/bids # Get project bids
```

## Bids
```
GET    /bids              # List bids (filter by user/project)
POST   /bids              # Submit bid
GET    /bids/{id}         # Get bid details
PUT    /bids/{id}         # Update bid
DELETE /bids/{id}         # Delete bid
POST   /bids/{id}/accept # Accept bid
```

## Payments
```
POST   /payments/initiate/mpesa  # Start M-Pesa payment
GET    /payments/transactions    # List transactions
GET    /payments/transactions/{id}  # Transaction details
```

## Notifications
```
GET    /notifications            # List notifications
PUT    /notifications/{id}/read  # Mark as read
PUT    /notifications/read-all   # Mark all as read
```

## Documents
```
POST   /documents/upload         # Upload file
GET    /documents/download/{id}  # Download file
DELETE /documents/{id}           # Delete file
```

## Common Headers
```
Authorization: Bearer <token>
Content-Type: application/json
```

## Example Request
```http
POST /projects
Authorization: Bearer abc123
Content-Type: application/json

{
  "title": "Website Redesign",
  "description": "Need a modern website",
  "category_id": 1,
  "location": "Nairobi",
  "budget": 50000
}
```

## Response Format
```json
{
  "status": "success",
  "data": {},
  "message": ""
}
```

## Error Format
```json
{
  "status": "error",
  "message": "Error description",
  "code": "ERROR_CODE"
}
```

## Status Codes
- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found
- 500: Server Error
