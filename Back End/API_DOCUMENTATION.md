# Jagedo Construction Platform API Documentation

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
    "email": "contractor@example.com",
    "name": "Sylvester Masinde",
    "role": "contractor",
    "location": "Nairobi, Kenya",
    "company_name": "Elite Builders Ltd",
    "profile_description": "Licensed general contractor specializing in residential and commercial construction",
    "nca_level": 5,
    "trade_licenses": ["NCA-12345", "NEMB-2023"],
    "specializations": ["Residential Construction", "Renovation"]
  }
}
```

---

## Construction Projects

### Create Construction Project
```http
POST /api/projects
```

**Request Body (multipart/form-data):**
- `title` (string, required): Project title (e.g., "Residential House Construction")
- `description` (string, required): Detailed project description
- `budget` (number, required): Estimated budget in local currency
- `location` (string, required): Project site address or coordinates
- `category_id` (integer, required): 
  - 1: Residential Construction
  - 2: Commercial Construction
  - 3: Renovation
  - 4: Civil Engineering
  - 5: Interior Design
- `project_type` (string, required): New Build/Renovation/Extension/etc.
- `property_size` (number): Size in square meters
- `expected_timeline` (number): Expected duration in weeks
- `drawings[]` (array of files): Architectural plans, blueprints, etc.
- `site_photos[]` (array of files): Photos of the construction site
- `required_documents[]` (array of files): Any additional documents (permits, surveys, etc.)

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
    "title": "3-Bedroom Bungalow Construction",
    "description": "Construction of a modern 3-bedroom bungalow with open plan living area and double garage",
    "status": "open",
    "project_type": "New Build",
    "property_size": 180,
    "budget": 8000000.00,
    "location": "Karen, Nairobi, Kenya",
    "expected_timeline": 36,
    "category": {
      "id": 1,
      "name": "Residential Construction"
    },
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
      "filename": "architectural_plans.pdf",
      "file_type": "application/pdf",
      "size": 5242880,
      "document_type": "architectural_drawing",
      "uploaded_at": "2025-05-21T10:15:00Z",
      "is_owner": true,
      "file_url": "/api/documents/1"
    },
    {
      "id": 2,
      "filename": "site_photos.zip",
      "file_type": "application/zip",
      "size": 15728640,
      "document_type": "site_photos",
      "uploaded_at": "2025-05-21T10:20:00Z",
      "is_owner": true,
      "file_url": "/api/documents/2"
    }
  ]
}
```

---

## Bids

### Submit Construction Bid
```http
POST /api/projects/{project_id}/bids
```

**Request Body:**
```json
{
  "amount": 7500000.00,
  "proposal": "Our company specializes in residential construction with 10+ years of experience. We propose to complete the project in 32 weeks using high-quality materials and skilled labor.",
  "timeline_weeks": 32,
  "materials_specification": [
    {
      "item": "Foundation",
      "specification": "Strip foundation with reinforced concrete"
    },
    {
      "item": "Walls",
      "specification": "Stone masonry with thermal insulation"
    }
  ],
  "workforce_plan": {
    "skilled_laborers": 6,
    "unskilled_laborers": 12,
    "supervisors": 2
  },
  "previous_similar_projects": [
    "4-Bedroom Villa in Runda (2024)",
    "Townhouse Development in Kitengela (2023)"
  ]
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
      "amount": 7500000.00,
      "currency": "KES",
      "proposal": "Our company specializes in residential construction with 10+ years of experience...",
      "status": "under_review",
      "timeline_weeks": 32,
      "submitted_at": "2025-05-21T11:30:00Z",
      "contractor": {
        "id": 2,
        "name": "Elite Builders Ltd",
        "contact_person": "John Kamau",
        "nca_level": 5,
        "years_experience": 15,
        "rating": 4.8,
        "completed_projects": 42,
        "trade_licenses": ["NCA-12345", "NEMB-2023"]
      },
      "key_personnel": [
        {
          "name": "Brian Mwenda",
          "role": "Site Engineer",
          "qualifications": ["BSc. Civil Engineering", "NCA-5"]
        }
      ]
    }
  ]
}
```

### Award Construction Contract
```http
POST /api/projects/{project_id}/award-contract
```

**Request Body:**
```json
{
  "bid_id": 1,
  "award_amount": 7450000.00,
  "contract_terms": "Standard JCT Construction Contract with amendments as per attached",
  "commencement_date": "2025-06-15",
  "practical_completion_date": "2025-12-15",
  "retention_percentage": 5,
  "payment_terms": "30 days from invoice",
  "liquidated_damages": 50000.00,
  "attachments": ["signed_contract.pdf"]
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Construction contract awarded successfully",
  "data": {
    "contract_id": "CON-2025-001",
    "bid_id": 1,
    "contractor_id": 2,
    "contractor_name": "Elite Builders Ltd",
    "award_amount": 7450000.00,
    "currency": "KES",
    "commencement_date": "2025-06-15",
    "practical_completion_date": "2025-12-15",
    "contract_document_url": "/api/contracts/CON-2025-001"
  }
}
```

---

## Construction Documents

### Download Construction Document
```http
GET /api/documents/{document_id}
```

**Query Parameters:**
- `download` (boolean, optional): Set to true to force file download

**Success Response:**
- Returns the file as an attachment with appropriate content-type

### Upload Construction Document
```http
POST /api/projects/{project_id}/documents
```

**Request Body (multipart/form-data):**
- `file` (file, required): The document file to upload
- `document_type` (string, required): Type of document (e.g., 'drawing', 'specification', 'permit', 'inspection_report')
- `revision` (string, optional): Document revision number/letter
- `issue_date` (string, optional): Date of issue (YYYY-MM-DD)
- `description` (string, optional): Brief description of the document

**Success Response (201 Created):**
```json
{
  "success": true,
  "message": "Document uploaded successfully",
  "data": {
    "document_id": 1,
    "filename": "structural_drawings_revB.pdf",
    "document_type": "drawing",
    "size": 5242880,
    "url": "/api/documents/1"
  }
}
```

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

## Construction Site Locations

### Search Construction Sites
```http
GET /api/places/autocomplete?query=construction site
```

**Query Parameters:**
- `query` (string, required): Search query (address, landmark, or coordinates)
- `location` (string, optional): "lat,lng" for biasing results to a specific area
- `radius` (number, optional): Search radius in meters (default: 50000)
- `types` (string, optional): Filter by place type (e.g., 'construction', 'building_construction')
- `country` (string, optional): Restrict results to a specific country (e.g., 'ke' for Kenya)

**Success Response (200 OK):**
```json
{
  "status": "success",
  "predictions": [
    {
      "description": "New Commercial Complex Site, Westlands, Nairobi",
      "place_id": "ChIJd8BlQ2BZwokRAFUEcm_qrcA",
      "types": ["construction", "establishment"],
      "structured_formatting": {
        "main_text": "New Commercial Complex Site",
        "secondary_text": "Westlands, Nairobi, Kenya"
      },
      "location": {
        "lat": -1.2657,
        "lng": 36.8022
      },
      "site_photos": [
        "/api/sites/123/photos/1"
      ]
    }
  ]
}
```

### Get Construction Site Details
```http
GET /api/sites/{site_id}
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "site": {
    "id": "site_12345",
    "name": "New Commercial Complex",
    "address": "Woodvale Grove, Westlands, Nairobi, Kenya",
    "coordinates": {
      "lat": -1.2657,
      "lng": 36.8022
    },
    "project_type": "Commercial Construction",
    "project_scope": "10-story office complex with 3-level basement parking",
    "project_status": "In Progress",
    "start_date": "2025-01-15",
    "target_completion": "2026-06-30",
    "contractor": "Elite Builders Ltd",
    "client": "Prestige Properties Ltd",
    "site_contact": {
      "name": "Michael Kamau",
      "role": "Site Manager",
      "phone": "+254712345678"
    },
    "site_photos": [
      {
        "id": "photo_1",
        "url": "/api/sites/123/photos/1",
        "caption": "Site preparation - Week 1",
        "date_taken": "2025-01-20T09:30:00Z"
      }
    ],
    "site_visits": [
      {
        "date": "2025-05-15",
        "purpose": "Monthly progress inspection",
        "inspector": "Jane Muthoni (NCA)",
        "status": "Scheduled"
      }
    ],
    "safety_rating": 4.5,
    "environmental_compliance": true,
    "permit_numbers": ["NCA-2025-0012", "NEMA-2025-0045"],
    "last_updated": "2025-05-20T15:30:00Z"
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
