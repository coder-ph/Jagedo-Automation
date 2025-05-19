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

3. **API Design**
   - RESTful endpoints
   - JSON-based request/response
   - Comprehensive error handling
   - CORS support for cross-origin requests

4. **Security Features**
   - Environment variable configuration
   - Input validation
   - JWT authentication
   - SQL injection prevention via SQLAlchemy

## Setup

1. Create a virtual environment:
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
   FLASK_APP=app.py
   FLASK_DEBUG=True
   DATABASE_URL=  # add external db url if any, otherwise leave empty
   SECRET_KEY=your-secret-key
   ```

4. Initialize the database:
   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. Run the application:
   ```bash
   flask run
   ```

### Test Endpoint
- `POST /api/test` - Test POST request with JSON body
- `GET /api/health` - API health status
