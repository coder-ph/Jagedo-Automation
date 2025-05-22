# Jagedo

## Architecture

1. **Application Factory Pattern**
   - Modular application initialization
   - Environment-based configuration
   - Extensible design

2. **Database Layer**
   - SQLAlchemy ORM for database operations
   - Flask-Migrate for database migrations
   - SQLite as default database 
   - Remote db configurable via DATABASE_URL

3. **File Storage**
   - Cloudinary integration for file storage
   - Fallback to local file system
   - Secure file uploads with validation
   - Support for multiple file types

4. **API Design**
   - RESTful endpoints
   - JSON-based request/response
   - Comprehensive error handling
   - CORS support for cross-origin requests

5. **Security Features**
   - Environment variable configuration
   - Input validation
   - JWT authentication
   - SQL injection prevention via SQLAlchemy
   - Secure file upload validation

## Setup

1. Create a virtual environment (optional):
   ```bash
   python -m venv venv
   source venv/bin/activate # On Windows: venv\Scripts\activate
   ```

   or 

   ```bash
   pipenv install
   pipenv shell
   ```

2. Install dependencies:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Set up environment variables (create .env file):
   ```bash
   # Flask Configuration
   FLASK_APP=app.py
   FLASK_DEBUG=True
   
   # Database Configuration
   DATABASE_URL=sqlite:///data-dev.sqlite
   
   # JWT Configuration
   JWT_SECRET_KEY=your-jwt-secret-key
   
   # Cloudinary Configuration (required for file uploads)
   CLOUDINARY_CLOUD_NAME=your_cloud_name
   CLOUDINARY_API_KEY=your_api_key
   CLOUDINARY_API_SECRET=your_api_secret
   CLOUDINARY_URL=cloudinary://your_api_key:your_api_secret@your_cloud_name
   
   # Storage Provider (set to 'cloudinary' or 'local')
   STORAGE_PROVIDER=cloudinary
   DATABASE_URL=  # add external db url if any, otherwise leave empty
   SECRET_KEY=your-secret-key
   ```

4. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```
5. Seed the database
   ```bash
   python ./seed.py
   ```

6. Run the application:
   ```bash
   flask run
   ```

## File Uploads

### Supported File Types
- Images: jpg, jpeg, png, gif, webp
- Documents: pdf, doc, docx, txt, rtf
- Spreadsheets: xls, xlsx, csv
- Presentations: ppt, pptx
- Archives: zip, rar, 7z
- Code: py, js, html, css, json, xml

### Uploading Files

```http
POST /api/documents/upload
Content-Type: multipart/form-data
Authorization: Bearer <your_jwt_token>

file: <file_data>
document_type: profile|bid|job|other
job_id: <optional_job_id>
bid_id: <optional_bid_id>
title: <optional_title>
description: <optional_description>
```

### Retrieving Files

```http
GET /api/documents/download/<attachment_id>
Authorization: Bearer <your_jwt_token>
```

## Running Tests

To run the test suite:

```bash
# Run all tests
pytest

# Run only Cloudinary tests
pytest tests/test_cloudinary.py -v
```

## Testing File Uploads

1. Set up your `.env` file with valid Cloudinary credentials
2. Run the application:
   ```bash
   flask run
   ```
3. Use a tool like Postman or cURL to test the upload endpoint:
   ```bash
   curl -X POST http://localhost:5000/api/documents/upload \
     -H "Authorization: Bearer <your_jwt_token>" \
     -F "file=@/path/to/your/file.jpg" \
     -F "document_type=profile"
   ```

### Test Endpoint
- `POST /api/test` - Test POST request with JSON body
- `GET /api/health` - API health status
