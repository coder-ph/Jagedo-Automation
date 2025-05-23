import os
import sys
from datetime import datetime
from faker import Faker
from werkzeug.security import generate_password_hash

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set environment variables before importing the app
os.environ['FLASK_ENV'] = 'development'
os.environ['GOOGLE_PLACES_API_KEY'] = 'dummy-key-for-seeding'

# Mock the SimplePlacesService before importing the app
from unittest.mock import MagicMock
sys.modules['app.services.simple_places_service'] = MagicMock()

# Now import the app and models
from app import create_app, db
from models import User, UserRole, Category, Skill

# Create the Flask application
app = create_app()

# Initialize Faker
fake = Faker()

def create_admin():
    """Create an admin user if one doesn't exist."""
    with app.app_context():
        admin = User.query.filter_by(email='admin@example.com').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@example.com',
                password=generate_password_hash('admin123'),
                first_name='Admin',
                last_name='User',
                phone_number='+254700000000',
                role=UserRole.ADMIN,
                is_verified=True,
                created_at=datetime.utcnow()
            )
            db.session.add(admin)
            db.session.commit()
            print("✓ Created admin user")
        return admin

def create_categories():
    """Create some sample categories."""
    with app.app_context():
        categories = [
            'Construction', 'Technology', 'Healthcare', 'Education',
            'Home Services', 'Automotive', 'Beauty & Wellness', 'Business Services'
        ]
        
        created = []
        for name in categories:
            if not Category.query.filter_by(name=name).first():
                category = Category(name=name)
                db.session.add(category)
                created.append(category)
        
        db.session.commit()
        print(f"✓ Created {len(created)} categories")
        return created

def create_skills(categories):
    """Create some sample skills."""
    with app.app_context():
        skills_data = {
            'Construction': ['Carpentry', 'Masonry', 'Plumbing', 'Electrical', 'Painting'],
            'Technology': ['Web Development', 'Mobile Development', 'Data Science', 'UI/UX Design'],
            'Healthcare': ['Nursing', 'Physiotherapy', 'Nutrition', 'First Aid'],
            'Education': ['Tutoring', 'Curriculum Design', 'Language Teaching'],
            'Home Services': ['Cleaning', 'Gardening', 'Pest Control', 'Appliance Repair'],
            'Automotive': ['Mechanic', 'Auto Body', 'Detailing', 'Tire Services'],
            'Beauty & Wellness': ['Hair Styling', 'Manicure', 'Massage', 'Makeup'],
            'Business Services': ['Accounting', 'Legal', 'Marketing', 'Consulting']
        }
        
        created = []
        for category in categories:
            for skill_name in skills_data.get(category.name, []):
                if not Skill.query.filter_by(name=skill_name).first():
                    skill = Skill(name=skill_name, category_id=category.id)
                    db.session.add(skill)
                    created.append(skill)
        
        db.session.commit()
        print(f"✓ Created {len(created)} skills")
        return created

def main():
    """Main function to run the seed script."""
    print("\n=== Starting Database Seeding ===\n")
    
    # Initialize the database
    with app.app_context():
        print("Dropping and recreating database tables...")
        db.drop_all()
        db.create_all()
        
        # Create initial data
        print("\nCreating initial data...")
        admin = create_admin()
        categories = create_categories()
        skills = create_skills(categories)
    
    print("\n=== Database Seeding Completed Successfully! ===\n")

if __name__ == '__main__':
    main()
