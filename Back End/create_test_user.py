from app import app, db
from models import User, UserRole
from werkzeug.security import generate_password_hash

def create_test_user():
    with app.app_context():
        # Check if user already exists
        if User.query.filter_by(email='test@example.com').first():
            print("Test user already exists")
            return
            
        # Create test user
        user = User(
            email='test@example.com',
            name='Test User',
            password_hash=generate_password_hash('test123'),
            role=UserRole.ADMIN,
            location='Nairobi'
        )
        db.session.add(user)
        db.session.commit()
        print("Test user created successfully")

if __name__ == "__main__":
    create_test_user()
