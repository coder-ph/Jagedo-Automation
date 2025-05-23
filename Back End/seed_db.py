import os
import sys
from unittest.mock import MagicMock

# Mock the SimplePlacesService before importing the app
sys.modules['app.services.simple_places_service'] = MagicMock()
from app.services.simple_places_service import SimplePlacesService
SimplePlacesService.return_value.autocomplete.return_value = []
SimplePlacesService.return_value.get_place_details.return_value = {}

# Set a dummy Google Places API key
os.environ['GOOGLE_PLACES_API_KEY'] = 'dummy-key-for-seeding'

# Now import the app and models
from app import create_app, db
from models import User, UserRole, Category, Skill
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_admin():
    # Check if admin already exists
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
        print("Created admin user")
    return admin

def create_categories():
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
    print(f"Created {len(created)} categories")
    return created

def create_skills():
    skills_data = {
        'Construction': ['Carpentry', 'Masonry', 'Plumbing', 'Electrical', 'Painting'],
        'Technology': ['Web Development', 'Mobile Development', 'Data Science', 'UI/UX Design'],
        'Healthcare': ['Nursing', 'Physiotherapy', 'Nutrition', 'First Aid'],
        'Education': ['Tutoring', 'Curriculum Design', 'Language Teaching'],
    }
    
    created = []
    for category_name, skill_names in skills_data.items():
        category = Category.query.filter_by(name=category_name).first()
        if category:
            for skill_name in skill_names:
                if not Skill.query.filter_by(name=skill_name).first():
                    skill = Skill(name=skill_name, category_id=category.id)
                    db.session.add(skill)
                    created.append(skill)
    
    db.session.commit()
    print(f"Created {len(created)} skills")
    return created

def seed_database():
    print("Starting database seeding...")
    
    # Create tables
    print("Creating database tables...")
    db.create_all()
    
    # Create admin user
    print("Creating admin user...")
    create_admin()
    
    # Create categories
    print("Creating categories...")
    create_categories()
    
    # Create skills
    print("Creating skills...")
    create_skills()
    
    print("\nDatabase seeding completed successfully!")

if __name__ == '__main__':
    # Create the Flask application
    app = create_app()
    
    # Push the application context
    with app.app_context():
        seed_database()
