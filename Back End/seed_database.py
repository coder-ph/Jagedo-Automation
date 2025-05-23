import os
import sys
from datetime import datetime, timedelta
from faker import Faker
from werkzeug.security import generate_password_hash

# Add the current directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set environment variables before importing the app
os.environ['FLASK_ENV'] = 'development'
os.environ['GOOGLE_PLACES_API_KEY'] = 'dummy-key-for-seeding'

# Now import the app and db
from app import create_app, db
from models import User, UserRole, Job, Category, Skill, ProfessionalSkill, Bid, JobStatus, BidStatus, Review, Message, Attachment, Notification

app = create_app()

# Initialize Faker
fake = Faker()

# Kenyan cities for location data
kenyan_cities = [
    "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Thika", "Malindi",
    "Kitale", "Garissa", "Nyeri", "Machakos", "Kericho", "Embu", "Naivasha"
]

def create_admin_user():
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
                phone_number=fake.phone_number(),
                role=UserRole.ADMIN,
                is_verified=True,
                created_at=datetime.utcnow()
            )
            db.session.add(admin)
            db.session.commit()
            print("Created admin user")
        return admin

def create_categories():
    """Create some sample categories."""
    with app.app_context():
        categories = [
            'Construction', 'Technology', 'Healthcare', 'Education',
            'Home Services', 'Automotive', 'Beauty & Wellness', 'Business Services'
        ]
        
        created_categories = []
        for name in categories:
            category = Category.query.filter_by(name=name).first()
            if not category:
                category = Category(name=name)
                db.session.add(category)
                created_categories.append(category)
        
        db.session.commit()
        print(f"Created {len(created_categories)} categories")
        return created_categories

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
        
        created_skills = []
        for category in categories:
            for skill_name in skills_data.get(category.name, []):
                skill = Skill.query.filter_by(name=skill_name).first()
                if not skill:
                    skill = Skill(name=skill_name, category_id=category.id)
                    db.session.add(skill)
                    created_skills.append(skill)
        
        db.session.commit()
        print(f"Created {len(created_skills)} skills")
        return created_skills

def main():
    """Main function to run the seed script."""
    with app.app_context():
        print("Dropping and recreating database tables...")
        db.drop_all()
        db.create_all()
        
        print("Creating admin user...")
        admin = create_admin_user()
        
        print("Creating categories...")
        categories = create_categories()
        
        print("Creating skills...")
        skills = create_skills(categories)
        
        print("\nDatabase seeding completed successfully!")

if __name__ == '__main__':
    main()
