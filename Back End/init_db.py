import os
import sys
import random
from datetime import datetime, timedelta
import random
import os
from unittest.mock import MagicMock
from werkzeug.security import generate_password_hash
from faker import Faker
from slugify.slugify import slugify
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text, func

# Set environment variables before importing the app
os.environ['FLASK_ENV'] = 'development'
os.environ['GOOGLE_PLACES_API_KEY'] = 'dummy-key-for-seeding'

# Mock services before importing the app
sys.modules['googleplaces'] = MagicMock()
sys.modules['app.services.places_service'] = MagicMock()
sys.modules['app.services.simple_places_service'] = MagicMock()

# Import the Flask app and models
from app import create_app, db
from app.models.user import User
from app.models.enums import UserRole, JobStatus, BidStatus
from app.models.notification import Notification, ProjectStatusHistory
from app.models.job import Job
from app.models.bid import Bid
from app.models.message import Review
from app.models.category import Category, Skill, ProfessionalSkill
from app.models.message import Message

# Initialize Faker with UK English for more realistic Kenyan names/addresses
fake = Faker('en_GB')

# Kenyan cities for realistic location data
KENYAN_CITIES = [
    'Nairobi', 'Mombasa', 'Kisumu', 'Nakuru', 'Eldoret', 'Thika', 'Malindi', 'Kitale',
    'Garissa', 'Kakamega', 'Nyeri', 'Meru', 'Kisii', 'Naivasha', 'Machakos', 'Nanyuki',
    'Kericho', 'Lamu', 'Isiolo', 'Narok', 'Bungoma', 'Busia', 'Embu', 'Kitui', 'Voi'
]

# Create the Flask application
app = create_app()

# Configure the app context
ctx = app.app_context()
ctx.push()

# Create tables if they don't exist
db.create_all()

# Create the uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def create_admin_user():
    """Create admin user if not exists."""
    with app.app_context():
        admin = User.query.filter_by(email='admin@example.com').first()
        if not admin:
            admin = User(
                name='Admin User',
                email='admin@example.com',
                password=generate_password_hash('admin123'),
                role=UserRole.ADMIN,
                phone='+254700000000',
                location='Nairobi',
                is_active=True,
                is_verified=True,
                created_at=datetime.utcnow()
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin user created")
        return admin

def create_sample_users(num_customers=50, num_professionals=100):
    """Create sample users (customers and professionals)."""
    customer_data = []
    professional_data = []
    
    print(f"Creating {num_customers} customers and {num_professionals} professionals...")
    
    # Create customers
    for i in range(num_customers):
        user_data = {
            'name': fake.name(),
            'email': f'customer{i}@example.com',
            'password': generate_password_hash('password123'),
            'phone': f'+2547{random.randint(10000000, 99999999)}',
            'role': UserRole.CUSTOMER,
            'location': random.choice(KENYAN_CITIES),
            'is_active': True,
            'is_verified': random.random() > 0.2,  # 80% verified
            'created_at': fake.date_time_between(start_date='-1y', end_date='-1m'),
            'profile_description': fake.paragraph(nb_sentences=2) if random.random() > 0.5 else None
        }
        customer_data.append(user_data)
    
    # Create professionals data
    skills = Skill.query.all()
    
    for i in range(num_professionals):
        prof_data = {
            'name': fake.name(),
            'email': f'pro{i}@example.com',
            'password': generate_password_hash('password123'),
            'phone': f'+2547{random.randint(10000000, 99999999)}',
            'role': UserRole.PROFESSIONAL,
            'location': random.choice(KENYAN_CITIES),
            'company_name': fake.company() if random.random() > 0.3 else None,
            'profile_description': fake.paragraph(nb_sentences=3),
            'is_active': True,
            'is_verified': random.random() > 0.2,  # 80% verified
            'created_at': fake.date_time_between(start_date='-1y', end_date='-1m'),
            'business_website': fake.url() if random.random() > 0.7 else None,
            'average_rating': round(random.uniform(3.0, 5.0), 1) if random.random() > 0.3 else 0.0,
            'skills': []
        }
        
        # Add random skills to professionals
        if skills:
            num_skills = random.randint(1, min(5, len(skills)))
            selected_skills = random.sample(skills, num_skills)
            
            for skill in selected_skills:
                prof_data['skills'].append({
                    'skill_id': skill.id,
                    'proficiency': random.choice(['Beginner', 'Intermediate', 'Advanced', 'Expert']),
                    'years_of_experience': random.randint(1, 10)
                })
        
        professional_data.append(prof_data)
    
    # Now create all users in a single transaction
    customer_ids = []
    professional_ids = []
    
    # Create customers
    for data in customer_data:
        user = User(**{k: v for k, v in data.items() if k != 'skills'})
        db.session.add(user)
        db.session.flush()  # Get the user ID
        customer_ids.append(user.id)
    
    # Create professionals with skills
    for data in professional_data:
        skills = data.pop('skills', [])
        user = User(**data)
        db.session.add(user)
        db.session.flush()  # Get the user ID
        professional_ids.append(user.id)
        
        # Add professional skills
        for skill_data in skills:
            prof_skill = ProfessionalSkill(
                user_id=user.id,
                **skill_data
            )
            db.session.add(prof_skill)
    
    db.session.commit()
    print(f"Created {len(customer_ids)} customers and {len(professional_ids)} professionals")
    
    return customer_ids, professional_ids

def create_sample_jobs(customer_ids, professional_ids=None, num_jobs=200):
    """Create sample jobs with realistic data.
    
    Args:
        customer_ids: List of customer IDs that can create jobs
        professional_ids: List of professional user IDs that can be assigned to jobs
        num_jobs: Number of jobs to create
    """
    if professional_ids is None:
        professional_ids = []
    print(f"Creating {num_jobs} sample jobs...")
    
    # First, check if we have any categories at all
    if Category.query.count() == 0:
        # Create parent categories
        construction = Category(name='Construction')
        technology = Category(name='Technology')
        healthcare = Category(name='Healthcare')
        education = Category(name='Education')
        home_services = Category(name='Home Services')
        automotive = Category(name='Automotive')
        beauty = Category(name='Beauty & Wellness')
        business = Category(name='Business Services')
        
        db.session.add_all([construction, technology, healthcare, education, 
                          home_services, automotive, beauty, business])
        db.session.flush()  # Get the IDs
        
        # Create subcategories
        construction_subcats = [
            Category(name='Carpentry', parent_id=construction.id),
            Category(name='Plumbing', parent_id=construction.id),
            Category(name='Electrical', parent_id=construction.id),
            Category(name='Masonry', parent_id=construction.id),
            Category(name='Roofing', parent_id=construction.id)
        ]
        
        tech_subcats = [
            Category(name='Web Development', parent_id=technology.id),
            Category(name='Mobile Development', parent_id=technology.id),
            Category(name='Data Science', parent_id=technology.id),
            Category(name='UI/UX Design', parent_id=technology.id),
            Category(name='DevOps', parent_id=technology.id)
        ]
        
        db.session.add_all(construction_subcats + tech_subcats)
        db.session.commit()
    
    # Get all non-parent categories
    categories = Category.query.filter(Category.parent_id.is_not(None)).all()
    
    if not categories:
        # Fallback: if for some reason we still don't have subcategories, create at least one
        parent = Category.query.first()
        if parent:
            default_cat = Category(name='General Services', parent_id=parent.id)
            db.session.add(default_cat)
            db.session.commit()
            categories = [default_cat]
    
    jobs = []
    
    for i in range(num_jobs):
        # Get a random customer ID directly
        customer_id = random.choice(customer_ids)
        category = random.choice(categories)
        
        # Generate job details
        title = f"{fake.bs().title()} {category.name} Services"
        description = f"{fake.paragraph(nb_sentences=3)}\n\n{fake.paragraph(nb_sentences=2)}"
        
        # Ensure we have a good distribution of job statuses
        # Let's make sure at least 30% of jobs are completed
        if i < 0.3 * num_jobs:  # First 30% of jobs will be completed
            status = JobStatus.COMPLETED
        else:
            status = random.choices(
                population=[JobStatus.OPEN, JobStatus.IN_PROGRESS, JobStatus.CANCELLED],
                weights=[0.6, 0.35, 0.05],
                k=1
            )[0]
            
        # Convert status to string for storage
        status = status.value if hasattr(status, 'value') else status
        
        # Generate timestamps based on status
        created_at = fake.date_time_between(start_date='-3m', end_date='now')
        
        if status in [JobStatus.IN_PROGRESS, JobStatus.COMPLETED, JobStatus.CANCELLED]:
            started_at = fake.date_time_between(start_date=created_at, end_date='now')
        else:
            started_at = None
            
        if status in [JobStatus.COMPLETED, JobStatus.CANCELLED]:
            completed_at = fake.date_time_between(start_date=started_at or created_at, end_date='now')
        else:
            completed_at = None
            
        job = Job(
            title=title,
            description=description,
            customer_id=customer_id,
            category_id=category.id,
            status=status,
            location=random.choice(KENYAN_CITIES),
            budget=random.choice([1000, 2000, 3000, 5000, 10000, 15000, 20000, 50000]),
            created_at=created_at
        )
        
        # Assign some jobs to professionals and mark as completed
        if status in [JobStatus.IN_PROGRESS, JobStatus.COMPLETED]:
            job.started_at = started_at
            job.assigned_contractor_id = random.choice(professional_ids) if professional_ids else None
            
            if status == JobStatus.COMPLETED:
                job.completed_at = completed_at
        
        db.session.add(job)
        jobs.append(job)
    
    db.session.commit()
    print(f"Created {len(jobs)} sample jobs")
    return jobs

def create_sample_bids(jobs, professional_ids, avg_bids_per_job=3):
    """Create sample bids on jobs.
    
    Args:
        jobs: List of Job objects
        professional_ids: List of professional user IDs
        avg_bids_per_job: Average number of bids per job
    """
    print(f"Creating sample bids (avg {avg_bids_per_job} per job)...")
    
    bids = []
    
    for job in jobs:
        # Determine number of bids for this job (variation around the average)
        num_bids = max(1, int(random.normalvariate(avg_bids_per_job, 1)))
        
        # Get professionals who aren't the job poster
        eligible_pros = [pid for pid in professional_ids if pid != job.customer_id]
        
        if not eligible_pros:
            continue
            
        # Select random professionals to bid
        num_bidders = min(num_bids, len(eligible_pros))
        bidders = random.sample(eligible_pros, num_bidders)
        
        for pro_id in bidders:
            # Generate bid details
            amount = float(job.budget) * random.uniform(0.7, 1.5)  # Bid within 70-150% of budget
            
            # Random bid status with weights
            status = random.choices(
                population=[BidStatus.PENDING, BidStatus.ACCEPTED, BidStatus.REJECTED],
                weights=[0.7, 0.2, 0.1],
                k=1
            )[0]
            
            # Create bid with required fields
            bid = Bid(
                job_id=job.id,
                professional_id=pro_id,
                amount=amount,
                proposal=fake.paragraph(nb_sentences=3),
                timeline_weeks=random.randint(1, 12),  # 1-12 weeks timeline
                status=status,
                created_at=fake.date_time_between(
                    start_date=job.created_at,
                    end_date='now'
                )
            )
            
            db.session.add(bid)
            bids.append(bid)
            
            # If bid is accepted, mark job as in progress
            if status == BidStatus.ACCEPTED:
                job.status = JobStatus.IN_PROGRESS
                job.assigned_contractor_id = pro_id
                
                # Add project status history
                history = ProjectStatusHistory(
                    project_id=job.id,
                    from_status=JobStatus.OPEN,
                    to_status=JobStatus.IN_PROGRESS,
                    changed_by=job.customer_id,
                    notes=f"Bid accepted from {pro_id}",
                    created_at=datetime.utcnow()
                )
                db.session.add(history)
    
    try:
        db.session.commit()
        print(f"Created {len(bids)} bids")
        return bids
    except Exception as e:
        print(f"Error committing bids: {e}")
        db.session.rollback()
        return []

def create_sample_reviews(jobs, num_reviews=300):
    """Create sample reviews for completed jobs."""
    with app.app_context():
        print(f"Creating up to {num_reviews} sample reviews...")
        print(f"Total jobs received: {len(jobs)}")
        
        # Debug: Print job statuses
        status_counts = {}
        for job in jobs:
            # Get status as string, handling both enum and string values
            status = job.status.value if hasattr(job.status, 'value') else str(job.status)
            status_counts[status] = status_counts.get(status, 0) + 1
        print(f"Job status counts: {status_counts}")
        
        # Find completed jobs by comparing status as string
        completed_jobs = [j for j in jobs if 
                         (hasattr(j.status, 'value') and j.status.value == 'completed') or 
                         (isinstance(j.status, str) and j.status.lower() == 'completed')]
        print(f"Found {len(completed_jobs)} completed jobs")
        
        if not completed_jobs:
            print("No completed jobs to review")
            return []
        
        reviews = []
        jobs_with_reviews = set()
        
        # Limit the number of reviews to a reasonable number per job
        max_reviews_per_job = 5
        max_possible_reviews = len(completed_jobs) * max_reviews_per_job
        num_reviews = min(num_reviews, max_possible_reviews)
        
        # Create a list of all possible job-reviewer pairs
        review_opportunities = []
        for job in completed_jobs:
            # Customer review of professional
            if job.assigned_contractor_id:
                review_opportunities.append((job, 'customer_to_pro'))
            
            # Professional review of customer
            review_opportunities.append((job, 'pro_to_customer'))
            
            # Optional: Reviews from other bidders (if any)
            if len(job.bids) > 1:
                for bid in job.bids:
                    if bid.status == BidStatus.REJECTED and bid.professional_id != job.assigned_contractor_id:
                        review_opportunities.append((job, 'bidder', bid.professional_id))
        
        # Shuffle the review opportunities
        random.shuffle(review_opportunities)
        
        # Take only the number of reviews requested
        review_opportunities = review_opportunities[:num_reviews]
        
        for review_info in review_opportunities:
            job = review_info[0]
            review_type = review_info[1]
            
            try:
                if review_type == 'customer_to_pro' and job.assigned_contractor_id:
                    # Customer reviews professional
                    review = Review(
                        job_id=job.id,
                        reviewer_id=job.customer_id,
                        reviewee_id=job.assigned_contractor_id,
                        rating=random.choices(
                            population=[1, 2, 3, 4, 5],
                            weights=[0.05, 0.1, 0.15, 0.3, 0.4],  # Mostly positive
                            k=1
                        )[0],
                        comment=fake.paragraph(nb_sentences=2),
                        created_at=fake.date_time_between(
                            start_date=job.completed_at,
                            end_date=job.completed_at + timedelta(days=14)  # Reviews within 2 weeks
                        )
                    )
                    reviews.append(review)
                    db.session.add(review)
                    
                elif review_type == 'pro_to_customer' and job.assigned_contractor_id:
                    # Professional reviews customer
                    review = Review(
                        job_id=job.id,
                        reviewer_id=job.assigned_contractor_id,
                        reviewee_id=job.customer_id,
                        rating=random.choices(
                            population=[3, 4, 5],  # Professionals usually rate customers well
                            weights=[0.1, 0.3, 0.6],
                            k=1
                        )[0],
                        comment=fake.paragraph(nb_sentences=2),
                        created_at=fake.date_time_between(
                            start_date=job.completed_at,
                            end_date=job.completed_at + timedelta(days=14)
                        )
                    )
                    reviews.append(review)
                    db.session.add(review)
                    
                elif review_type == 'bidder' and len(review_info) > 2:
                    # Other bidders can review the customer
                    bidder_id = review_info[2]
                    review = Review(
                        job_id=job.id,
                        reviewer_id=bidder_id,
                        reviewee_id=job.customer_id,
                        rating=random.choices(
                            population=[1, 2, 3, 4, 5],
                            weights=[0.1, 0.2, 0.3, 0.2, 0.2],  # More neutral distribution
                            k=1
                        )[0],
                        comment=fake.paragraph(nb_sentences=1),
                        created_at=fake.date_time_between(
                            start_date=job.completed_at - timedelta(days=7),  # Can review before completion
                            end_date=job.completed_at + timedelta(days=7)
                        )
                    )
                    reviews.append(review)
                    db.session.add(review)
                    
            except Exception as e:
                print(f"Error creating review: {e}")
                db.session.rollback()
        
        try:
            db.session.commit()
            print(f"Created {len(reviews)} reviews")
            return reviews
        except Exception as e:
            print(f"Error committing reviews: {e}")
            db.session.rollback()
            return []

def create_sample_notifications(users, jobs, num_notifications=500):
    """Create sample notifications for users."""
    with app.app_context():
        print(f"Creating {num_notifications} sample notifications...")
        notifications = []
        
        if not users or not jobs:
            print("No users or jobs available to create notifications")
            return []
        
        notification_types = [
            'message_received', 'bid_received', 'bid_accepted', 'bid_rejected',
            'review_received', 'job_posted', 'job_assigned', 'job_completed',
            'payment_received', 'payment_sent', 'milestone_reached', 'dispute_opened'
        ]
        
        # Create a list to store notification data before creating them
        notification_data = []
        
        for _ in range(num_notifications):
            user = random.choice(users)
            notification_type = random.choice(notification_types)
            created_at = fake.date_time_between(start_date='-30d', end_date='now')
            
            # Initialize context and message templates
            context = {}
            title = ""
            message = ""
            
            try:
                if notification_type == 'message_received':
                    # Only customers and professionals can receive messages
                    if user.role not in [UserRole.CUSTOMER, UserRole.PROFESSIONAL]:
                        continue
                        
                    from_user = random.choice([u for u in users if u.id != user.id])
                    title = f"New message from {from_user.name}"
                    message = fake.sentence()
                    context.update({
                        'from_user_id': from_user.id,
                        'conversation_id': f"conv_{random.randint(1000, 9999)}",
                        'preview': message[:50] + '...'
                    })
                    
                elif notification_type in ['bid_received', 'bid_accepted', 'bid_rejected']:
                    # Only customers receive bid notifications
                    if user.role != UserRole.CUSTOMER:
                        continue
                        
                    job = random.choice([j for j in jobs if j.customer_id == user.id] or [None])
                    if not job:
                        continue
                        
                    if notification_type == 'bid_received':
                        title = "New Bid Received"
                        message = f"You've received a new bid on your job: {job.title}"
                        context.update({
                            'job_id': job.id,
                            'bid_id': random.randint(1000, 9999),
                            'bid_amount': float(job.budget) * random.uniform(0.7, 1.5)
                        })
                    else:  # accepted or rejected
                        bid = random.choice(job.bids) if job.bids else None
                        if not bid:
                            continue
                            
                        if notification_type == 'bid_accepted':
                            title = "Bid Accepted!"
                            message = f"Your bid for '{job.title}' has been accepted!"
                        else:
                            title = "Bid Not Selected"
                            message = f"Your bid for '{job.title}' was not selected this time."
                            
                        context.update({
                            'job_id': job.id,
                            'bid_id': bid.id,
                            'job_title': job.title
                        })
                
                elif notification_type == 'review_received':
                    title = "New Review"
                    message = f"You've received a new {random.choice(['5-star', '4-star', '3-star', '2-star', '1-star'])} review!"
                    context.update({
                        'rating': random.randint(1, 5),
                        'reviewer': fake.name(),
                        'comment': fake.paragraph(nb_sentences=1)
                    })
                    
                elif notification_type == 'job_posted':
                    # Only professionals receive job posting notifications
                    if user.role != UserRole.PROFESSIONAL:
                        continue
                        
                    job = random.choice(jobs)
                    title = "New Job Matching Your Skills"
                    message = f"New job posted: {job.title} in {job.location}"
                    context.update({
                        'job_id': job.id,
                        'job_title': job.title,
                        'budget': float(job.budget),
                        'location': job.location
                    })
                    
                elif notification_type == 'payment_received':
                    amount = random.uniform(1000, 50000)
                    title = "Payment Received"
                    message = f"You've received a payment of KES {amount:,.2f}"
                    context.update({
                        'amount': amount,
                        'transaction_id': f"txn_{random.randint(100000, 999999)}",
                        'status': 'completed'
                    })
                
                # Add more notification types as needed...
                
                # Create the notification
                notification = Notification(
                    user_id=user.id,
                    notification_type=notification_type,
                    title=title,
                    message=message,
                    is_read=random.random() > 0.3,  # 70% chance of being read
                    context=context,
                    created_at=created_at,
                    updated_at=created_at
                )
                
                # Mark as read if it's an old notification
                if (datetime.utcnow() - created_at).days > 7:
                    notification.is_read = True
                
                notifications.append(notification)
                db.session.add(notification)
                
                # Occasionally create multiple notifications in quick succession
                if random.random() > 0.8:  # 20% chance
                    for _ in range(random.randint(1, 3)):
                        similar_notif = Notification(
                            user_id=user.id,
                            notification_type=notification_type,
                            title=title,
                            message=message,
                            is_read=notification.is_read,
                            context=context.copy(),
                            created_at=created_at + timedelta(minutes=random.randint(1, 60))
                        )
                        notifications.append(similar_notif)
                        db.session.add(similar_notif)
                
            except Exception as e:
                print(f"Error creating notification: {e}")
                db.session.rollback()
        
        try:
            db.session.commit()
            print(f"Created {len(notifications)} notifications")
            return notifications
        except Exception as e:
            print(f"Error committing notifications: {e}")
            db.session.rollback()
            return []

def init_db():
    """Initialize the database with sample data."""
    with app.app_context():
        try:
            print("\n=== Starting database initialization ===\n")
            
            # Drop and recreate all tables
            print("Dropping all tables...")
            db.drop_all()
            
            print("Creating all tables...")
            db.create_all()
            
            # Create admin user
            admin = create_admin_user()
            
            # Create sample users
            customer_ids, professional_ids = create_sample_users(num_customers=50, num_professionals=100)
            
            # Create sample jobs
            jobs = create_sample_jobs(customer_ids, professional_ids=professional_ids, num_jobs=200)
            
            print("Creating sample bids...")
            bids = create_sample_bids(jobs, professional_ids, avg_bids_per_job=3)
            
            # Create sample reviews
            reviews = create_sample_reviews(jobs, num_reviews=300)
            
            # Create sample notifications
            all_user_ids = customer_ids + professional_ids
            notifications = create_sample_notifications(all_user_ids, jobs, num_notifications=500)
            
            print("\n=== Database initialized successfully! ===")
            print(f"Admin user: admin@example.com / admin123")
            print(f"Sample customer: customer1@example.com / password123")
            print(f"Sample professional: pro1@example.com / password123")
            
            print("\nSummary of created data:")
            print(f"- Users: {len(customer_ids)} customers, {len(professional_ids)} professionals")
            print(f"- Jobs: {len(jobs)} (various statuses)")
            print(f"- Bids: {len(bids)} (average {len(bids)/len(jobs):.1f} per job)")
            print(f"- Reviews: {len(reviews)}")
            print(f"- Notifications: {len(notifications)}")
            
            # Commit all changes
            db.session.commit()
            return True
            
        except Exception as e:
            db.session.rollback()
            print(f"\n!!! Error initializing database: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            # Ensure the session is closed to prevent connection leaks
            if db.session:
                db.session.close()

if __name__ == "__main__":
    init_db()
