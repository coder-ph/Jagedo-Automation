from datetime import datetime, timedelta, timezone
from faker import Faker
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError
from .extensions import db
from .models.user import User
from .models.job import Job
from .models.bid import Bid
from .models.category import Category, Skill, ProfessionalSkill
from .models.message import Message
from .models.notification import Notification
from .models.attachment import Attachment
from .models.payment import PaymentTransaction, PaymentMethod
from .models.enums import UserRole, JobStatus, BidStatus, PaymentStatus, NotificationType
from app import create_app
import random

fake = Faker()

# Kenyan cities for location data
KENYAN_CITIES = [
    "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Thika", "Malindi",
    "Kitale", "Garissa", "Nyeri", "Machakos", "Kericho", "Embu", "Naivasha"
]

def init_db():
    """Initialize the database by creating all tables."""
    db.drop_all()  # Drop all existing tables
    db.create_all()  # Create all tables
    print("Database initialized successfully")

def create_categories():
    """Create initial categories and subcategories."""
    parent_categories = ['Construction', 'Technology', 'Healthcare', 'Education', 'Professional Services']
    
    # Create parent categories
    for name in parent_categories:
        category = Category(name=name)
        db.session.add(category)
    db.session.commit()

    # Create child categories
    child_categories = {
        'Construction': ['Roofing', 'Plumbing', 'Electrical', 'Carpentry', 'Masonry'],
        'Technology': ['Software Development', 'Network Engineering', 'Data Science', 'UI/UX Design'],
        'Healthcare': ['Dentistry', 'Pediatrics', 'General Medicine', 'Nursing'],
        'Education': ['Tutoring', 'Curriculum Design', 'Special Education', 'Language Teaching'],
        'Professional Services': ['Legal Services', 'Accounting', 'Consulting', 'Marketing']
    }

    for parent_name, children in child_categories.items():
        parent = Category.query.filter_by(name=parent_name).first()
        for child in children:
            category = Category(name=child, parent_id=parent.id)
            db.session.add(category)
    
    db.session.commit()
    return Category.query.all()

def create_skills(categories):
    """Create skills for each category."""
    skills_map = {
        'Roofing': ['Shingle Installation', 'Leak Repair', 'Roof Inspection', 'Metal Roofing'],
        'Plumbing': ['Pipe Repair', 'Fixture Installation', 'Drain Cleaning', 'Water Heater Installation'],
        'Electrical': ['Wiring Installation', 'Circuit Breaker Repair', 'Lighting Installation', 'Panel Upgrades'],
        'Carpentry': ['Custom Furniture', 'Cabinet Making', 'Wood Framing', 'Trim Work'],
        'Masonry': ['Brick Laying', 'Concrete Work', 'Stone Masonry', 'Tile Installation'],
        'Software Development': ['Python', 'JavaScript', 'Database Design', 'API Development'],
        'Network Engineering': ['Network Security', 'Cisco Configuration', 'VPN Setup', 'Cloud Infrastructure'],
        'Data Science': ['Machine Learning', 'Data Analysis', 'Statistical Modeling', 'Big Data'],
        'UI/UX Design': ['User Interface Design', 'User Experience', 'Wireframing', 'Prototyping'],
        'Dentistry': ['Teeth Cleaning', 'Fillings', 'Orthodontics', 'Dental Surgery'],
        'Pediatrics': ['Child Wellness Check', 'Vaccinations', 'Nutrition Counseling', 'Developmental Assessment'],
        'General Medicine': ['Primary Care', 'Chronic Disease Management', 'Preventive Care', 'Health Screening'],
        'Nursing': ['Patient Care', 'Medical Procedures', 'Health Education', 'Care Planning'],
        'Tutoring': ['Math Tutoring', 'Science Tutoring', 'Language Arts', 'Test Preparation'],
        'Curriculum Design': ['Lesson Planning', 'Educational Standards', 'Assessment Creation', 'Learning Materials'],
        'Special Education': ['Individual Education Plans', 'Learning Support', 'Behavioral Intervention', 'Inclusive Education'],
        'Language Teaching': ['ESL Teaching', 'Language Immersion', 'Grammar Instruction', 'Conversation Practice'],
        'Legal Services': ['Contract Law', 'Corporate Law', 'Family Law', 'Intellectual Property'],
        'Accounting': ['Tax Preparation', 'Financial Planning', 'Auditing', 'Bookkeeping'],
        'Consulting': ['Business Strategy', 'Process Improvement', 'Change Management', 'Market Analysis'],
        'Marketing': ['Digital Marketing', 'Content Strategy', 'Brand Development', 'Social Media Management']
    }

    for category_name, skills in skills_map.items():
        category = Category.query.filter_by(name=category_name).first()
        if category:
            for skill in skills:
                skill_obj = Skill(name=skill, category_id=category.id)
                db.session.add(skill_obj)
    
    db.session.commit()
    return Skill.query.all()

def create_users(num_users=20):
    users = []
    
    # Create admin user
    admin = User(
        role=UserRole.ADMIN,
        name="Admin User",
        email="admin@admin.com",
        _password=generate_password_hash("password123"),
        phone=fake.phone_number(),
        location=fake.city(),
        is_verified=True,
        is_active=True
    )
    users.append(admin)
    db.session.add(admin)
    
    # Create regular users
    for _ in range(num_users):
        is_professional = random.choice([True, False])
        user = User(
            role=UserRole.PROFESSIONAL if is_professional else UserRole.CUSTOMER,
            name=fake.name(),
            email=fake.email(),
            _password=generate_password_hash("password123"),
            phone=fake.phone_number(),
            location=fake.city(),
            is_verified=random.choice([True, False]),
            is_active=True
        )
        
        if is_professional:
            user.company_name = fake.company()
            user.business_description = fake.text(max_nb_chars=500)
            user.business_address = fake.address()
            user.business_phone = fake.phone_number()
            user.business_website = fake.url()
            user.profile_description = fake.text(max_nb_chars=300)
            user.nca_level = random.randint(1, 5)
            user.average_rating = round(random.uniform(3.0, 5.0), 1)
            user.total_ratings = random.randint(5, 50)
        
        users.append(user)
        db.session.add(user)
    
    db.session.commit()
    return users

def create_jobs(users, categories, num_jobs=30):
    jobs = []
    customers = [u for u in users if u.role == UserRole.CUSTOMER]
    professionals = [u for u in users if u.role == UserRole.PROFESSIONAL]
    
    for _ in range(num_jobs):
        customer = random.choice(customers)
        status = random.choice(list(JobStatus))
        
        # Only assign contractor if job is in progress or completed
        assigned_contractor = None
        if status in [JobStatus.IN_PROGRESS, JobStatus.COMPLETED]:
            assigned_contractor = random.choice(professionals)
        
        # Set payment status and reference based on job status
        payment_status = random.choice(list(PaymentStatus))
        payment_reference = f"PAY-{fake.uuid4()}" if payment_status == PaymentStatus.COMPLETED else None
        payment_date = fake.date_time_this_year() if payment_status == PaymentStatus.COMPLETED else None
        
        job = Job(
            title=fake.catch_phrase(),
            description=fake.text(max_nb_chars=1000),
            category_id=random.choice(categories).id,
            customer_id=customer.id,
            location=random.choice(KENYAN_CITIES),
            status=status,
            payment_status=payment_status,
            payment_reference=payment_reference,
            payment_date=payment_date,
            assigned_contractor_id=assigned_contractor.id if assigned_contractor else None,
            budget=round(random.uniform(100, 5000), 2)
        )
        jobs.append(job)
        db.session.add(job)
    
    db.session.commit()
    return jobs

def create_bids(jobs, users, num_bids=50):
    bids = []
    professionals = [u for u in users if u.role == UserRole.PROFESSIONAL]
    
    # Create a set to track which job-professional pairs have already been used
    used_pairs = set()
    
    for _ in range(num_bids):
        # Keep trying until we find an unused job-professional pair
        while True:
            job = random.choice(jobs)
            professional = random.choice(professionals)
            pair = (job.id, professional.id)
            
            if pair not in used_pairs:
                used_pairs.add(pair)
                break
        
        bid = Bid(
            job_id=job.id,
            professional_id=professional.id,
            amount=round(random.uniform(float(job.budget) * 0.8, float(job.budget) * 1.2), 2),
            proposal=fake.text(max_nb_chars=500),
            status=random.choice(list(BidStatus)),
            timeline_weeks=random.randint(1, 12)
        )
        bids.append(bid)
        db.session.add(bid)
    
    db.session.commit()
    return bids

def create_messages(users, num_messages=100):
    messages = []
    
    for _ in range(num_messages):
        sender = random.choice(users)
        receiver = random.choice([u for u in users if u.id != sender.id])
        
        message = Message(
            sender_id=sender.id,
            receiver_id=receiver.id,
            message=fake.text(max_nb_chars=200),
            read_at=fake.date_time_this_year() if random.choice([True, False]) else None
        )
        messages.append(message)
        db.session.add(message)
    
    db.session.commit()
    return messages

def create_notifications(users, jobs, num_notifications=50):
    notifications = []
    
    for _ in range(num_notifications):
        user = random.choice(users)
        job = random.choice(jobs)
        
        notification = Notification(
            user_id=user.id,
            title=fake.sentence(),
            message=fake.text(max_nb_chars=100),
            content=fake.text(max_nb_chars=200),
            read=random.choice([True, False]),
            notification_type=random.choice(list(NotificationType))
        )
        notifications.append(notification)
        db.session.add(notification)
    
    db.session.commit()
    return notifications

def create_payments(jobs, users, num_payments=30):
    payments = []
    
    for _ in range(num_payments):
        job = random.choice(jobs)
        user = random.choice(users)
        
        payment = PaymentTransaction(
            user_id=user.id,
            project_id=job.id,
            amount=float(job.budget),
            currency='KES',
            status=random.choice(list(PaymentStatus)),
            method=random.choice(list(PaymentMethod)),
            reference=f"PAY-{fake.uuid4()}",
            phone_number=fake.phone_number() if random.choice([True, False]) else None,
            mpesa_receipt=fake.uuid4() if random.choice([True, False]) else None,
            payment_metadata={'source': 'seed_data'}
        )
        payments.append(payment)
        db.session.add(payment)
    
    db.session.commit()
    return payments

def seed_database():
    """Main function to seed the database with all data"""
    print("Starting database seeding...")
    
    # Clear existing data
    print("Clearing existing data...")
    db.session.query(ProfessionalSkill).delete()
    db.session.query(Skill).delete()
    db.session.query(Category).delete()
    db.session.query(Bid).delete()
    db.session.query(Job).delete()
    db.session.query(Message).delete()
    db.session.query(Notification).delete()
    db.session.query(Attachment).delete()
    db.session.query(PaymentTransaction).delete()
    db.session.query(User).delete()
    db.session.commit()
    
    # Create categories
    print("Creating categories...")
    categories = create_categories()
    
    # Create users
    print("Creating users...")
    users = create_users()
    
    # Create jobs
    print("Creating jobs...")
    jobs = create_jobs(users, categories)
    
    # Create bids
    print("Creating bids...")
    bids = create_bids(jobs, users)
    
    # Create messages
    print("Creating messages...")
    messages = create_messages(users)
    
    # Create notifications
    print("Creating notifications...")
    notifications = create_notifications(users, jobs)
    
    # Create payments
    print("Creating payments...")
    payments = create_payments(jobs, users)
    
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_database()