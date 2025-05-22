from app import app, db, bcrypt
from models import *

def init_db():
    with app.app_context():
        # Drop all tables first
        db.drop_all()
        
        # Create all database tables
        db.create_all()
        
        # Create admin user
        admin = User(
            email='admin@example.com',
            name='Admin User',
            password_hash=bcrypt.generate_password_hash('admin123').decode('utf-8'),
            role=UserRole.ADMIN,
            location='Nairobi',
            nca_level=8,
            is_active=True
        )
        db.session.add(admin)
        
        # Create test user
        user = User(
            email='test@example.com',
            name='Test User',
            password_hash=bcrypt.generate_password_hash('test123').decode('utf-8'),
            role=UserRole.CUSTOMER,
            location='Nairobi',
            is_active=True
        )
        db.session.add(user)
        
        # Commit all changes
        db.session.commit()
        print("Database initialized with admin and test users")

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully")
