# BuildPro API - Construction Project Management

## Base URL
`http://localhost:5001/api`

## Authentication
```
POST /auth/register  # Register contractor or client
POST /auth/login     # Login to get access token
POST /auth/refresh   # Refresh access token
GET  /auth/me        # Get current user profile
```

## Construction Projects
```
GET    /projects           # List construction projects
POST   /projects           # Create new construction project
GET    /projects/{id}      # Get project details
PUT    /projects/{id}      # Update project
GET    /projects/{id}/bids # Get project bids
```

## Contractor Bids
```
GET    /bids              # List bids (filter by contractor/project)
POST   /bids              # Submit bid for project
GET    /bids/{id}         # Get bid details
PUT    /bids/{id}         # Update bid
DELETE /bids/{id}         # Withdraw bid
POST   /bids/{id}/accept  # Accept contractor's bid
```

## Project Payments
```
POST   /payments/initiate/mpesa  # Process construction payment
GET    /payments/transactions    # List payment history
GET    /payments/milestones     # Manage payment milestones
```

## Project Communication
```
GET    /messages           # Project messages
POST   /messages           # Send message
GET    /notifications      # Project notifications
PUT    /notifications/read # Mark as read
```

## Construction Documents
```
POST   /documents/blueprints  # Upload blueprints
POST   /documents/permits     # Upload permits
POST   /documents/reports     # Upload progress reports
GET    /documents/{id}        # Download document
```

## Common Headers
```
Authorization: Bearer <token>
Content-Type: application/json
```

## Example: Create Construction Project
```http
POST /projects
Authorization: Bearer abc123
Content-Type: application/json

{
  "title": "Residential House Construction",
  "description": "2-story residential house with 4 bedrooms",
  "category_id": 3,  // Residential Construction
  "location": "Nairobi West",
  "budget": 15000000,
  "start_date": "2023-07-01",
  "duration_weeks": 36
}
```

## Response Format
```json
{
  "status": "success",
  "data": {
    "project_id": 123,
    "reference_number": "BP-2023-1234"
  },
  "message": "Project created successfully"
}
```

## Error Format
```json
{
  "status": "error",
  "message": "Invalid project details",
  "code": "INVALID_INPUT",
  "details": {
    "budget": "Must be at least 1,000,000"
  }
}
```

## Status Codes
- 200: Success
- 201: Resource Created
- 400: Bad Request (validation errors)
- 401: Unauthorized
- 403: Forbidden (insufficient permissions)
- 404: Resource Not Found
- 500: Internal Server Error
