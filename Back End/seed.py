import random
import os
from faker import Faker
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_caching import Cache
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set a dummy Google Places API key in the environment
os.environ['GOOGLE_PLACES_API_KEY'] = 'dummy-key-for-seeding'

# Create a minimal Flask app for seeding
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

# Initialize extensions
db = SQLAlchemy()
cache = Cache()
jwt = JWTManager()
migrate = Migrate()
cors = CORS()

# Initialize extensions with the app
db.init_app(app)
cache.init_app(app)
jwt.init_app(app)
migrate.init_app(app, db)
cors.init_app(app)

# Import models after db is created to avoid circular imports
from models import User, UserRole, Job, Category, Skill, ProfessionalSkill, Bid, JobStatus, BidStatus, Review, Message, Attachment, Notification

# Mock the SimplePlacesService to avoid needing the Google Places API key
from unittest.mock import MagicMock
SimplePlacesService = MagicMock()
SimplePlacesService.return_value.autocomplete.return_value = []
SimplePlacesService.return_value.get_place_details.return_value = {}

# Push the application context
app.app_context().push()

fake = Faker()

kenyan_cities = [
        "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Thika", "Malindi",
        "Kitale", "Garissa", "Nyeri", "Machakos", "Kericho", "Embu", "Naivasha"
    ]

def create_categories_and_skills():
    """Create parent and child categories with associated skills."""
    print("Creating categories and skills...")
    
    # Parent categories
    parent_categories = [
        'Construction', 'Technology', 'Healthcare', 'Education',
        'Home Services', 'Automotive', 'Beauty & Wellness', 'Business Services'
    ]
    
    # Create parent categories
    for name in parent_categories:
        if not Category.query.filter_by(name=name, parent_id=None).first():
            db.session.add(Category(name=name))
    db.session.commit()

    # Child categories with their parent categories
    child_categories = {
        'Construction': [
            'Roofing', 'Plumbing', 'Electrical', 'Masonry', 'Carpentry',
            'Painting', 'Flooring', 'Landscaping'
        ],
        'Technology': [
            'Software Development', 'Web Development', 'Mobile App Development',
            'Network Engineering', 'IT Support', 'Data Analysis', 'Cybersecurity'
        ],
        'Healthcare': [
            'Dentistry', 'Pediatrics', 'Physiotherapy', 'Nutrition',
            'Mental Health', 'Home Healthcare', 'Alternative Medicine'
        ],
        'Education': [
            'Tutoring', 'Curriculum Design', 'Language Lessons', 'Test Prep',
            'Music Lessons', 'Art Classes', 'Professional Training'
        ],
        'Home Services': [
            'Cleaning', 'Moving', 'Pest Control', 'Appliance Repair',
            'Interior Design', 'Gardening', 'Home Organization'
        ],
        'Automotive': [
            'Car Repair', 'Car Wash', 'Auto Detailing', 'Towing',
            'Car Audio Installation', 'Auto Glass Repair'
        ],
        'Beauty & Wellness': [
            'Hair Styling', 'Makeup', 'Massage Therapy', 'Nail Care',
            'Skincare', 'Barber Services', 'Spa Treatments'
        ],
        'Business Services': [
            'Accounting', 'Legal Services', 'Marketing', 'Graphic Design',
            'Content Writing', 'Virtual Assistance', 'Business Consulting'
        ]
    }
    
    # Create child categories
    for parent_name, children in child_categories.items():
        parent = Category.query.filter_by(name=parent_name, parent_id=None).first()
        if not parent:
            print(f"Parent category not found: {parent_name}")
            continue
            
        for child_name in children:
            if not Category.query.filter_by(name=child_name, parent_id=parent.id).first():
                db.session.add(Category(name=child_name, parent_id=parent.id))
    db.session.commit()

    # Skills for each category
    skills_map = {
        # Construction
        'Roofing': ['Shingle Installation', 'Leak Repair', 'Roof Inspection', 'Gutter Installation', 'Roof Replacement'],
        'Plumbing': ['Pipe Repair', 'Fixture Installation', 'Drain Cleaning', 'Water Heater Installation', 'Sewer Line Repair'],
        'Electrical': ['Wiring Installation', 'Circuit Breaker Repair', 'Lighting Installation', 'Panel Upgrades', 'Generator Installation'],
        'Masonry': ['Brick Laying', 'Concrete Work', 'Stone Work', 'Chimney Repair', 'Retaining Walls'],
        'Carpentry': ['Framing', 'Trim Work', 'Deck Building', 'Cabinet Installation', 'Custom Furniture'],
        'Painting': ['Interior Painting', 'Exterior Painting', 'Wallpaper Installation', 'Faux Finishes', 'Deck Staining'],
        'Flooring': ['Hardwood Installation', 'Tile Work', 'Carpet Installation', 'Laminate Flooring', 'Floor Refinishing'],
        'Landscaping': ['Lawn Care', 'Garden Design', 'Irrigation Systems', 'Tree Trimming', 'Hardscaping'],
        
        # Technology
        'Software Development': ['Python', 'JavaScript', 'Java', 'C#', 'PHP', 'Ruby', 'Go'],
        'Web Development': ['React', 'Vue.js', 'Angular', 'Node.js', 'Django', 'Flask', 'Laravel'],
        'Mobile App Development': ['iOS Development', 'Android Development', 'React Native', 'Flutter', 'Xamarin'],
        'Network Engineering': ['Network Security', 'Cisco Configuration', 'VPN Setup', 'Wireless Networking', 'Network Monitoring'],
        'IT Support': ['Help Desk Support', 'Hardware Troubleshooting', 'Software Installation', 'System Administration', 'Data Recovery'],
        'Data Analysis': ['SQL', 'Python Data Analysis', 'R', 'Data Visualization', 'Machine Learning'],
        'Cybersecurity': ['Penetration Testing', 'Security Auditing', 'Incident Response', 'Security Compliance', 'Ethical Hacking'],
        
        # Healthcare
        'Dentistry': ['Teeth Cleaning', 'Fillings', 'Orthodontics', 'Tooth Extraction', 'Dental Implants'],
        'Pediatrics': ['Child Wellness Check', 'Vaccinations', 'Nutrition Counseling', 'Developmental Screening', 'Sick Visits'],
        'Physiotherapy': ['Rehabilitation', 'Sports Injury Treatment', 'Post-Surgical Recovery', 'Pain Management', 'Mobility Training'],
        'Nutrition': ['Meal Planning', 'Weight Management', 'Sports Nutrition', 'Dietary Counseling', 'Eating Disorder Support'],
        'Mental Health': ['Counseling', 'Therapy', 'Stress Management', 'Anxiety Treatment', 'Depression Support'],
        'Home Healthcare': ['Elderly Care', 'Post-Hospital Care', 'Medication Management', 'Mobility Assistance', 'Companion Care'],
        'Alternative Medicine': ['Acupuncture', 'Chiropractic', 'Herbal Medicine', 'Ayurveda', 'Homeopathy'],
        
        # Education
        'Tutoring': ['Math Tutoring', 'Science Tutoring', 'Language Arts', 'Test Prep', 'Homework Help'],
        'Curriculum Design': ['Lesson Planning', 'Educational Standards', 'Assessment Creation', 'E-Learning Development', 'Instructional Design'],
        'Language Lessons': ['English', 'Spanish', 'French', 'Mandarin', 'German', 'Japanese', 'Sign Language'],
        'Test Prep': ['SAT/ACT Prep', 'GRE/GMAT Prep', 'LSAT Prep', 'MCAT Prep', 'Professional Certification Exams'],
        'Music Lessons': ['Piano', 'Guitar', 'Violin', 'Vocals', 'Drums', 'Music Theory'],
        'Art Classes': ['Drawing', 'Painting', 'Sculpture', 'Digital Art', 'Photography'],
        'Professional Training': ['Leadership Development', 'Public Speaking', 'Time Management', 'Project Management', 'Technical Skills Training']
    }
    
    # Create skills for each category
    for category_name, skills in skills_map.items():
        category = Category.query.filter_by(name=category_name).first()
        if not category:
            print(f"Category not found: {category_name}")
            continue
            
        for skill_name in skills:
            if not Skill.query.filter_by(name=skill_name, category_id=category.id).first():
                db.session.add(Skill(name=skill_name, category_id=category.id))
    
    db.session.commit()
    print("Categories and skills created successfully.")

def create_users(num_customers=25, num_professionals=50):
    """Create admin, customer, and professional users with realistic data."""
    print("Creating users...")
    
    # Clear existing users except admin
    db.session.query(User).filter(User.role != UserRole.ADMIN).delete(synchronize_session=False)
    
    # Common password for all demo users
    password = "Password123!"
    password_hash = generate_password_hash(password)
    
    # Create admin user if not exists
    admin = User.query.filter_by(email="admin@jagedo.com").first()
    if not admin:
        admin = User(
            role=UserRole.ADMIN,
            name="Admin User",
            email="admin@jagedo.com",
            _password=password_hash,
            phone="+254700000000",
            location="Nairobi",
            company_name="Jagedo Admin",
            profile_description="System Administrator with full access to the platform.",
            is_verified=True,
            is_active=True,
            created_at=datetime.utcnow() - timedelta(days=365),
            updated_at=datetime.utcnow()
        )
        db.session.add(admin)
    
    # Create customers
    for i in range(1, num_customers + 1):
        location = random.choice(kenyan_cities)
        customer = User(
            role=UserRole.CUSTOMER,
            name=f"Customer {i} {fake.last_name()}",
            email=f"customer{i}@jagedo.com",
            _password=password_hash,
            phone=f"+2547{random.randint(10000000, 99999999)}",
            location=location,
            company_name=fake.company() if random.random() > 0.7 else None,
            profile_description=f"Customer based in {location}. {fake.paragraph()}",
            is_verified=random.choices([True, False], weights=[0.8, 0.2])[0],
            is_active=random.choices([True, False], weights=[0.9, 0.1])[0],
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 365)),
            updated_at=datetime.utcnow()
        )
        db.session.add(customer)
    
    # Create professionals
    for i in range(1, num_professionals + 1):
        location = random.choice(kenyan_cities)
        business_name = fake.company()
        
        professional = User(
            role=UserRole.PROFESSIONAL,
            name=f"Professional {i} {fake.last_name()}",
            email=f"pro{i}@jagedo.com",
            _password=password_hash,
            phone=f"+2547{random.randint(10000000, 99999999)}",
            location=location,
            company_name=business_name,
            business_name=business_name,
            business_description=f"Professional {business_name} based in {location}. {fake.paragraph()}",
            business_address=f"{random.randint(100, 999)} {fake.street_name()}, {location}",
            business_phone=f"+2547{random.randint(10000000, 99999999)}",
            business_website=f"https://{business_name.lower().replace(' ', '')}.com",
            business_logo=random.choice(BUSINESS_LOGOS) if random.random() > 0.5 else None,
            profile_description=f"Professional service provider at {business_name}. {fake.paragraph()}",
            is_verified=random.choices([True, False], weights=[0.7, 0.3])[0],
            is_active=random.choices([True, False], weights=[0.85, 0.15])[0],
            average_rating=round(random.uniform(3.0, 5.0), 1),
            total_ratings=random.randint(0, 100),
            successful_bids=random.randint(0, 50),
            total_bids=random.randint(0, 100),
            created_at=datetime.utcnow() - timedelta(days=random.randint(1, 365)),
            updated_at=datetime.utcnow()
        )
        db.session.add(professional)
    
    db.session.commit()
    print(f"Created {User.query.count()} users (1 admin, {num_customers} customers, {num_professionals} professionals)")
    print(f"Admin credentials: Email: admin@jagedo.com, Password: {password}")

def assign_professional_skills():
    """Assign relevant skills to professionals based on categories."""
    print("Assigning skills to professionals...")
    
    professionals = User.query.filter_by(role=UserRole.PROFESSIONAL).all()
    categories = Category.query.filter(Category.parent_id.isnot(None)).all()
    
    # Group skills by category for easier access
    skills_by_category = {}
    for category in categories:
        skills = Skill.query.filter_by(category_id=category.id).all()
        if skills:
            skills_by_category[category.id] = skills
    
    for pro in professionals:
        # Each professional gets 1-3 categories
        num_categories = random.randint(1, 3)
        selected_categories = random.sample(categories, min(num_categories, len(categories)))
        
        for category in selected_categories:
            if category.id not in skills_by_category:
                continue
                
            skills = skills_by_category[category.id]
            if not skills:
                continue
                
            # Each professional gets 2-5 skills per category
            num_skills = random.randint(2, min(5, len(skills)))
            selected_skills = random.sample(skills, num_skills)
            
            for skill in selected_skills:
                # Check if the professional already has this skill
                existing = ProfessionalSkill.query.filter_by(
                    professional_id=pro.id,
                    skill_id=skill.id
                ).first()
                
                if not existing:
                    years_exp = random.randint(1, 15)
                    proficiency = random.choice(['Beginner', 'Intermediate', 'Advanced', 'Expert'])
                    
                    pro_skill = ProfessionalSkill(
                        professional_id=pro.id,
                        skill_id=skill.id,
                        years_experience=years_exp,
                        proficiency_level=proficiency,
                        is_certified=random.choice([True, False]),
                        certification_authority=fake.company() if random.choice([True, False]) else None,
                        created_at=datetime.utcnow() - timedelta(days=random.randint(1, 365)),
                        updated_at=datetime.utcnow()
                    )
                    db.session.add(pro_skill)
    
    db.session.commit()
    print(f"Assigned skills to {len(professionals)} professionals")

def create_jobs(num_jobs=50):
    """Create realistic job postings with various statuses and details."""
    print("Creating jobs...")
    
    # Clear existing jobs and related data
    db.session.query(Job).delete()
    db.session.commit()
    
    customers = User.query.filter_by(role=UserRole.CUSTOMER).all()
    categories = Category.query.filter(Category.parent_id.isnot(None)).all()
    
    job_titles = [
        "Looking for a professional to help with",
        "Need expert assistance with",
        "Urgent: Professional required for",
        "Hiring specialist for",
        "Project: Professional needed for"
    ]
    
    job_status_weights = {
        'open': 0.5,
        'in_progress': 0.3,
        'completed': 0.15,
        'cancelled': 0.05
    }
    
    for i in range(1, num_jobs + 1):
        customer = random.choice(customers)
        category = random.choice(categories)
        
        # Generate realistic job title and description
        skill = random.choice(Skill.query.filter_by(category_id=category.id).all() or [None])
        title = f"{random.choice(job_titles)} {skill.name if skill else category.name.lower()}"
        
        # Generate realistic job description
        description = f"""
        <p>I'm looking for a skilled professional to help me with {skill.name if skill else category.name.lower()}.
        {fake.paragraph(nb_sentences=3)}</p>
        
        <h4>Project Details:</h4>
        <ul>
            <li>Location: {customer.location}</li>
            <li>Timeline: {random.choice(['ASAP', 'Within 1 week', 'Within 2 weeks', 'Flexible'])}</li>
            <li>Budget: KES {random.randint(1000, 50000):,}</li>
        </ul>
        
        <h4>Requirements:</h4>
        <ul>
            <li>{fake.sentence()}</li>
            <li>{fake.sentence()}</li>
            <li>{fake.sentence()}</li>
        </ul>
        
        <p>{fake.paragraph(nb_sentences=2)}</p>
        """
        
        # Determine job status with weighted probability
        status = random.choices(
            list(job_status_weights.keys()),
            weights=list(job_status_weights.values())
        )[0]
        
        # Generate dates
        created_at = datetime.utcnow() - timedelta(days=random.randint(1, 90))
        deadline = created_at + timedelta(days=random.randint(1, 30))
        
        # For completed/cancelled jobs, ensure dates make sense
        if status in ['completed', 'cancelled']:
            deadline = created_at + timedelta(days=random.randint(1, 30))
        
        job = Job(
            title=title[:100],
            description=description,
            category_id=category.id,
            customer_id=customer.id,
            location=customer.location,
            latitude=random.uniform(-4.0, 4.0),  # Roughly within Kenya
            longitude=random.uniform(33.0, 42.0),  # Roughly within Kenya
            budget=random.choice([
                random.randint(1000, 5000),    # Small jobs
                random.randint(5001, 20000),   # Medium jobs
                random.randint(20001, 100000), # Large jobs
            ]),
            status=status,
            job_type=random.choice(['one_time', 'ongoing', 'contract']),
            experience_level=random.choice(['entry', 'intermediate', 'expert']),
            created_at=created_at,
            updated_at=datetime.utcnow(),
            deadline=deadline,
            is_urgent=random.random() > 0.8,
            is_featured=random.random() > 0.9,
            views=random.randint(0, 1000),
            applications_count=0  # Will be updated when bids are created
        )
        
        # Add job skills
        skills = Skill.query.filter_by(category_id=category.id).order_by(func.random()).limit(random.randint(1, 5)).all()
        for skill in skills:
            job.skills_required.append(skill)
        
        # Add job attachments (20% chance)
        if random.random() > 0.8:
            num_attachments = random.randint(1, 3)
            for _ in range(num_attachments):
                attachment = JobAttachment(
                    job=job,
                    file_url=random.choice([
                        'https://example.com/documents/specs.pdf',
                        'https://example.com/images/project.jpg',
                        'https://example.com/documents/requirements.docx'
                    ]),
                    file_type=random.choice(['pdf', 'image', 'doc']),
                    created_at=datetime.utcnow()
                )
                db.session.add(attachment)
        
        db.session.add(job)
    
    db.session.commit()
    print(f"Created {num_jobs} jobs with various statuses and details")

def create_bids():
    """Create realistic bids from professionals on open jobs."""
    print("Creating bids...")
    
    # Clear existing bids
    db.session.query(Bid).delete()
    db.session.commit()
    
    professionals = User.query.filter_by(role=UserRole.PROFESSIONAL).all()
    open_jobs = Job.query.filter(Job.status == 'open').all()
    
    if not open_jobs:
        print("No open jobs found to create bids for.")
        return
    
    if not professionals:
        print("No professionals found to create bids.")
        return
    
    bid_count = 0
    
    for job in open_jobs:
        # Get job category and skills
        job_skills = job.skills_required
        
        # Find professionals with matching skills
        matching_pros = []
        if job_skills:
            # Get professionals with at least one matching skill
            skill_ids = [s.id for s in job_skills]
            matching_pros = db.session.query(User).join(
                ProfessionalSkill, 
                User.id == ProfessionalSkill.professional_id
            ).filter(
                ProfessionalSkill.skill_id.in_(skill_ids),
                User.role == UserRole.PROFESSIONAL
            ).distinct().all()
        
        # If no matching professionals, use all professionals
        if not matching_pros:
            matching_pros = professionals
        
        # Determine number of bids for this job (weighted towards fewer bids)
        num_bids = random.choices(
            [1, 2, 3, 4, 5, 6, 7, 8],
            weights=[0.2, 0.3, 0.2, 0.15, 0.08, 0.04, 0.02, 0.01]
        )[0]
        num_bids = min(num_bids, len(matching_pros))
        
        # Select random professionals who haven't bid on this job yet
        bidders = random.sample(matching_pros, num_bids)
        
        # Sort bidders (earlier bidders get better rates)
        random.shuffle(bidders)
        
        for i, bidder in enumerate(bidders):
            # Calculate bid amount (earlier bidders have better rates)
            bid_multiplier = 0.7 + (i * 0.05)  # 70% for first bidder, up to 95% for last
            bid_amount = job.budget * random.uniform(bid_multiplier - 0.1, bid_multiplier + 0.1)
            bid_amount = round(bid_amount / 100) * 100  # Round to nearest 100
            
            # Generate bid message
            messages = [
                f"Hello! I'm interested in your {job.title.lower()}. "
                f"I have {random.randint(1, 10)}+ years of experience in this field. "
                f"I can complete this for KES {bid_amount:,}.",
                
                f"Hi there! I'd love to help with your {job.title.lower()}. "
                f"My rate is KES {bid_amount:,} for this job. Looking forward to working with you!",
                
                f"Professional {job.category.name.lower()} specialist here. "
                f"I can handle this project for KES {bid_amount:,}. "
                f"I'm available to start {random.choice(['immediately', 'next week', 'as soon as possible'])}.",
                
                f"I have experience with similar {job.category.name.lower()} projects. "
                f"My bid is KES {bid_amount:,}. Feel free to contact me for more details.",
                
                f"Hello! I noticed your {job.title.lower()} and I believe I'm a great fit. "
                f"I can complete this for KES {bid_amount:,}. Looking forward to your response!"
            ]
            
            # Determine bid status (most are pending, some are accepted/rejected)
            status_weights = {
                'pending': 0.8,
                'accepted': 0.15,
                'rejected': 0.05,
                'withdrawn': 0.0  # Will be set separately
            }
            
            # Only one accepted bid per job
            if any(b.status == 'accepted' for b in job.bids):
                status_weights['accepted'] = 0.0
                status_weights['pending'] = 0.9
                status_weights['rejected'] = 0.1
            
            status = random.choices(
                list(status_weights.keys()),
                weights=list(status_weights.values())
            )[0]
            
            # Create the bid
            bid = Bid(
                job_id=job.id,
                professional_id=bidder.id,
                amount=bid_amount,
                status=status,
                message=random.choice(messages),
                is_hourly=random.random() > 0.8,  # 20% chance of hourly rate
                estimated_hours=random.randint(1, 40) if random.random() > 0.8 else None,
                delivery_time=random.randint(1, 30),  # Days to complete
                created_at=job.created_at + timedelta(hours=random.randint(1, 168)),  # Within 1 week of job posting
                updated_at=datetime.utcnow()
            )
            
            # If this bid is accepted, update the job
            if status == 'accepted':
                job.status = 'in_progress'
                job.assigned_to = bidder.id
                job.assigned_at = datetime.utcnow()
                job.budget = bid_amount  # Update budget to accepted bid amount
            
            db.session.add(bid)
            bid_count += 1
            
            # Print progress every 10 bids
            if bid_count % 10 == 0:
                db.session.commit()
                print(f"Created {bid_count} bids...")
    
    db.session.commit()
    print(f"Created {bid_count} bids across {len(open_jobs)} jobs")

def create_reviews():
    """Create realistic reviews for completed jobs."""
    print("Creating reviews...")
    
    # Clear existing reviews
    db.session.query(Review).delete()
    db.session.commit()
    
    # Get completed jobs with accepted bids
    completed_jobs = Job.query.filter_by(status='completed').all()
    
    if not completed_jobs:
        print("No completed jobs found to create reviews for.")
        return
    
    review_count = 0
    
    # Common review templates for different ratings (5 is best, 1 is worst)
    review_templates = {
        5: [
            "{professional} did an outstanding job! {details} I would definitely hire them again.",
            "Exceptional work by {professional}. {details} Highly recommended!",
            "I'm extremely satisfied with the work done by {professional}. {details}",
            "{professional} went above and beyond my expectations. {details} 5 stars!",
            "Professional, punctual, and excellent work quality. {details} Will hire again!"
        ],
        4: [
            "Good work by {professional}. {details} Overall a positive experience.",
            "{professional} did a great job. {details} Would recommend.",
            "Satisfied with the work. {details} {professional} was professional and delivered as promised.",
            "Good experience overall. {details} {professional} communicated well and completed the job.",
            "The work was completed as expected. {details} Would hire {professional} again."
        ],
        3: [
            "Average experience. {details} The work was acceptable but there's room for improvement.",
            "{professional} did an okay job. {details} The work met my basic expectations.",
            "The work was completed, but there were some issues. {details}",
            "An average experience overall. {details} The job got done but could have been better.",
            "{professional} was professional but the work was just average. {details}"
        ],
        2: [
            "I was not completely satisfied with the work. {details} Expected better quality.",
            "{professional} didn't fully meet my expectations. {details} The work was below average.",
            "There were several issues with the work. {details} Disappointed with the results.",
            "The work was completed but the quality was poor. {details}",
            "Wouldn't hire {professional} again. {details} The work was subpar."
        ],
        1: [
            "Terrible experience. {details} Would not recommend {professional} to anyone.",
            "The work was not completed as agreed. {details} Very disappointed.",
            "{professional} did a horrible job. {details} I had to hire someone else to fix it.",
            "Waste of time and money. {details} The work was completely unacceptable.",
            "Never again. {details} {professional} was unprofessional and the work was terrible."
        ]
    }
    
    # Details to include in reviews
    details_templates = [
        "They were very professional and completed the work on time.",
        "The quality of work was excellent and exceeded my expectations.",
        "Communication was clear throughout the project.",
        "They showed up on time and completed the work efficiently.",
        "The final result was exactly what I was looking for.",
        "They were very knowledgeable and provided great suggestions.",
        "The work area was left clean and tidy after completion.",
        "They were very patient and addressed all my concerns.",
        "The project was completed within the agreed timeline.",
        "I appreciated their attention to detail and craftsmanship.",
        "There were some delays but they kept me informed throughout.",
        "The work was good but took longer than expected.",
        "There were a few issues but they were resolved quickly.",
        "The quality was acceptable but I expected better for the price.",
        "Communication could have been better during the project.",
        "The work was completed but required some follow-up.",
        "There were some misunderstandings about the scope of work.",
        "The final result was different from what we initially discussed.",
        "They didn't show up on the scheduled day without notice.",
        "The work was incomplete and I had to hire someone else to finish it.",
        "The quality of work was very poor and didn't meet basic standards.",
        "They were unprofessional and difficult to communicate with.",
        "The project went way over budget without proper authorization.",
        "They damaged my property and refused to take responsibility.",
        "I had to constantly follow up to get updates on the project."
    ]
    
    for job in completed_jobs:
        # Get the accepted bid for this job
        accepted_bid = Bid.query.filter_by(job_id=job.id, status='accepted').first()
        if not accepted_bid:
            continue
            
        professional = User.query.get(accepted_bid.professional_id)
        if not professional:
            continue
            
        # Determine rating (weighted towards positive reviews)
        rating = random.choices(
            [1, 2, 3, 4, 5],
            weights=[0.05, 0.1, 0.15, 0.3, 0.4]  # 70% 4-5 star reviews
        )[0]
        
        # Select review details based on rating
        if rating >= 4:
            # Positive details for 4-5 star reviews
            details = random.sample(details_templates[:15], 2)
        elif rating == 3:
            # Neutral details for 3 star reviews
            details = random.sample(details_templates[10:17], 2)
        else:
            # Negative details for 1-2 star reviews
            details = random.sample(details_templates[15:], 2)
        
        # Format the review
        review_text = random.choice(review_templates[rating]).format(
            professional=professional.name.split()[0],  # First name only
            details=' '.join(details)
        )
        
        # Create the review
        review = Review(
            rating=rating,
            comment=review_text,
            job_id=job.id,
            professional_id=professional.id,
            customer_id=job.customer_id,
            created_at=job.updated_at + timedelta(hours=random.randint(1, 24)),
            is_visible=True,
            response=fake.sentence() if random.random() > 0.7 else None,
            response_date=datetime.utcnow() if random.random() > 0.7 else None
        )
        
        db.session.add(review)
        review_count += 1
        
        # Update professional's rating
        if professional.average_rating:
            # Weighted average with previous ratings
            total_ratings = professional.total_ratings or 1
            professional.average_rating = (
                (professional.average_rating * total_ratings) + rating
            ) / (total_ratings + 1)
            professional.total_ratings = total_ratings + 1
        else:
            professional.average_rating = rating
            professional.total_ratings = 1
    
    db.session.commit()
    print(f"Created {review_count} reviews for {len(completed_jobs)} completed jobs")

def create_messages(num_messages=20):
    jobs = Job.query.all()
    users = User.query.all()
    for _ in range(num_messages):
        job = random.choice(jobs) if random.choice([True, False]) else None
        if job:
            customer_id = job.customer_id
            bids = Bid.query.filter_by(job_id=job.id).all()
            professionals = [b.professional_id for b in bids]
            participants = [customer_id] + professionals
            if not participants:
                continue
            sender_id = random.choice(participants)
            valid_receivers = [p for p in participants if p != sender_id]
            if not valid_receivers:  # Skip if no valid receivers
                continue
            receiver_id = random.choice(valid_receivers)
        else:
            sender, receiver = random.sample(users, 2)
            sender_id = sender.id
            receiver_id = receiver.id
        message = Message(
            message=fake.paragraph(),
            sender_id=sender_id,
            receiver_id=receiver_id,
            job_id=job.id if job else None,
            created_at=fake.date_time_this_year()
        )
        db.session.add(message)
    db.session.commit()

def create_attachments(num_attachments=30):
    jobs = Job.query.all()
    bids = Bid.query.all()
    users = User.query.all()
    
    # Define some common file extensions
    file_extensions = ['pdf', 'docx', 'jpg', 'png', 'txt']
    
    for _ in range(min(num_attachments, 30)):  # Limit to 30 attachments
        try:
            # Choose a random user to be the uploader
            uploaded_by = random.choice(users)
            
            # Choose what to attach to (job, bid, or user profile)
            attach_to = random.choice(['job', 'bid', 'user'])
            job = random.choice(jobs) if attach_to in ['job', 'bid'] and jobs else None
            bid = random.choice(bids) if attach_to == 'bid' and bids else None
            
            # If attaching to a bid, get the associated job and user
            if bid:
                job = Job.query.get(bid.job_id)
                user = db.session.get(User, bid.professional_id)
            elif job:
                user = random.choice(users)
            else:
                user = random.choice(users)
            
            # Generate a realistic filename
            file_ext = random.choice(file_extensions)
            filename = f"{fake.word()}_{fake.random_int(1, 1000)}.{file_ext}"
            
            # Create the attachment
            attachment = Attachment(
                file_url=fake.image_url(),
                uploaded_at=fake.date_time_this_year(),
                uploaded_by=uploaded_by.id,
                filename=filename,
                job_id=job.id if job else None,
                bid_id=bid.id if bid else None,
                user_id=user.id
            )
            db.session.add(attachment)
            db.session.flush()  # Flush to catch any integrity errors immediately
            
        except Exception as e:
            print(f"Error creating attachment: {e}")
            db.session.rollback()
    
    try:
        db.session.commit()
        print(f"Created {min(num_attachments, 30)} attachments")
    except Exception as e:
        print(f"Error committing attachments: {e}")
        db.session.rollback()

def create_notifications(num_notifications=100):
    users = User.query.all()
    jobs = Job.query.all()
    
    notification_types = [
        ('New Job Posted', 'A new job matching your skills has been posted!'),
        ('Bid Accepted', 'Your bid has been accepted!'),
        ('New Message', 'You have a new message'),
        ('Job Completed', 'Your job has been marked as completed'),
        ('Payment Received', 'Payment has been processed for your work'),
        ('Profile Updated', 'Your profile has been updated successfully'),
        ('New Review', 'You have received a new review'),
        ('Reminder', 'Don\'t forget to complete your profile'),
        ('System Update', 'New features available in your dashboard'),
        ('Security Alert', 'New login detected on your account')
    ]
    
    for _ in range(min(num_notifications, 100)):  # Limit to 100 notifications
        try:
            user = random.choice(users)
            job = random.choice(jobs) if jobs and random.random() > 0.3 else None
            
            # Choose a random notification type
            title, message_template = random.choice(notification_types)
            
            # Customize the message based on the title
            if 'Job' in title and job:
                message = f"{message_template}: {job.title}"
            else:
                message = message_template
                
            notification = Notification(
                content=message,  # Update content field
                read=random.choice([True, False]),
                created_at=fake.date_time_this_year(),
                user_id=user.id,
                job_id=job.id if job else None,
                title=title,
                message=message,
                notification_type=title.lower().replace(' ', '_')
            )
            db.session.add(notification)
            db.session.flush()
            
        except Exception as e:
            print(f"Error creating notification: {e}")
            db.session.rollback()
    
    try:
        db.session.commit()
        print(f"Created {min(num_notifications, 100)} notifications")
    except Exception as e:
        print(f"Error committing notifications: {e}")
        db.session.rollback()

def main():
    """Main function to run the seed script."""
    with app.app_context():
        print("Dropping and recreating database tables...")
        db.drop_all()
        db.create_all()
        
        # Create initial data
        create_categories_and_skills()
        create_users()
        assign_professional_skills()
        create_jobs()
        create_bids()

        print("Creating reviews...")
        create_reviews()

        print("Creating messages...")
        create_messages()

        print("Creating attachments...")
        create_attachments()

        print("Creating notifications...")
        create_notifications()

        print("Database populated with fake data!")

if __name__ == '__main__':
    main()