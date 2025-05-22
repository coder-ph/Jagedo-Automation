from app import app, db, bcrypt
from models import User, UserRole

def create_admin_user():
    with app.app_context():
        # Check if admin already exists
        admin = User.query.filter_by(email='admin@example.com').first()
        if admin:
            print("Admin user already exists")
            return
        
        # Create admin user
        hashed_password = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin = User(
            name='Admin User',
            email='admin@example.com',
            password_hash=hashed_password,
            role=UserRole.ADMIN,
            location='Nairobi',
            company_name='Admin Company',
            profile_description='System Administrator',
            nca_level=8,
            is_active=True
        )
        
        db.session.add(admin)
        db.session.commit()
        print("Admin user created successfully")
        print("Email: admin@example.com")
        print("Password: admin123")

if __name__ == "__main__":
    create_admin_user()
