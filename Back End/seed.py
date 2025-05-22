import random
from faker import Faker
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from app import app 
from models import db, User, UserRole, Job, Category, Skill, ProfessionalSkill, Bid, JobStatus, BidStatus, Review, Message, Attachment, Notification

fake = Faker()

kenyan_cities = [
        "Nairobi", "Mombasa", "Kisumu", "Nakuru", "Eldoret", "Thika", "Malindi",
        "Kitale", "Garissa", "Nyeri", "Machakos", "Kericho", "Embu", "Naivasha"
    ]

def create_categories_and_skills():
    parent_categories = ['Construction', 'Technology', 'Healthcare', 'Education']
    for name in parent_categories:
        db.session.add(Category(name=name))
    db.session.commit()

    child_categories = {
        'Construction': ['Roofing', 'Plumbing', 'Electrical'],
        'Technology': ['Software Development', 'Network Engineering'],
        'Healthcare': ['Dentistry', 'Pediatrics'],
        'Education': ['Tutoring', 'Curriculum Design']
    }
    for parent_name, children in child_categories.items():
        parent = Category.query.filter_by(name=parent_name).first()
        for child in children:
            db.session.add(Category(name=child, parent_id=parent.id))
    db.session.commit()

    skills_map = {
        'Roofing': ['Shingle Installation', 'Leak Repair', 'Roof Inspection'],
        'Plumbing': ['Pipe Repair', 'Fixture Installation', 'Drain Cleaning'],
        'Electrical': ['Wiring Installation', 'Circuit Breaker Repair', 'Lighting Installation'],
        'Software Development': ['Python', 'JavaScript', 'Database Design'],
        'Network Engineering': ['Network Security', 'Cisco Configuration', 'VPN Setup'],
        'Dentistry': ['Teeth Cleaning', 'Fillings', 'Orthodontics'],
        'Pediatrics': ['Child Wellness Check', 'Vaccinations', 'Nutrition Counseling'],
        'Tutoring': ['Math Tutoring', 'Science Tutoring', 'Language Arts'],
        'Curriculum Design': ['Lesson Planning', 'Educational Standards', 'Assessment Creation']
    }
    for category_name, skills in skills_map.items():
        category = Category.query.filter_by(name=category_name).first()
        for skill in skills:
            db.session.add(Skill(name=skill, category_id=category.id))
    db.session.commit()

def create_users(num_customers=10, num_professionals=10):
    password = "password123"  # This will be the password for all users
    bcrypt = Bcrypt()
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    # Create admin user
    admin = User(
        role=UserRole.ADMIN,
        name="Admin User",
        email="admin@admin.com",
        password_hash=password_hash,
        location=random.choice(kenyan_cities),
        profile_description="System Administrator"
    )
    db.session.add(admin)
    
    # Create customers
    for _ in range(num_customers):
        customer = User(
            role=UserRole.CUSTOMER,
            name=fake.name(),
            email=fake.unique.email(),
            password_hash=password_hash,
            company_name=fake.company() if random.choice([True, False]) else None,
            location=random.choice(kenyan_cities),
            profile_description=fake.paragraph() if random.random() < 0.5 else None
        )
        db.session.add(customer)
    
    # Create professionals
    for _ in range(num_professionals):
        professional = User(
            role=UserRole.PROFESSIONAL,
            name=fake.name(),
            email=fake.unique.email(),
            password_hash=password_hash,
            company_name=fake.company() if random.choice([True, False]) else None,
            location=random.choice(kenyan_cities),
            profile_description=fake.paragraph()
        )
        db.session.add(professional)
    
    db.session.commit()

def assign_professional_skills():
    professionals = User.query.filter_by(role=UserRole.PROFESSIONAL).all()
    child_categories = Category.query.filter(Category.parent_id.isnot(None)).all()
    
    for pro in professionals:
        category = random.choice(child_categories)
        skills = Skill.query.filter_by(category_id=category.id).all()
        if skills:
            num_skills = random.randint(2, 3)
            selected_skills = random.sample(skills, min(num_skills, len(skills)))
            for skill in selected_skills:
                ps = ProfessionalSkill(
                    professional_id=pro.id,
                    skill_id=skill.id,
                    certified=random.choice([True, False]),
                    years_experience=random.randint(1, 20),
                    nca_ratings=random.choice([f'NCA {i}' for i in range(1, 9)] + [None])
                )
                db.session.add(ps)
    db.session.commit()

def create_jobs(num_jobs=20):
    customers = User.query.filter_by(role=UserRole.CUSTOMER).all()
    child_categories = Category.query.filter(Category.parent_id.isnot(None)).all()
    
    for _ in range(num_jobs):
        customer = random.choice(customers)
        category = random.choice(child_categories)
        job = Job(
            title=fake.sentence(nb_words=3),
            description=fake.text(),
            category_id=category.id,
            customer_id=customer.id,
            location=random.choice(kenyan_cities),
            status=random.choice([JobStatus.OPEN, JobStatus.OPEN, JobStatus.OPEN, JobStatus.IN_PROGRESS, JobStatus.COMPLETED]),
            budget=fake.random_int(min=500, max=10000),
            created_at=fake.date_time_this_year()
        )
        db.session.add(job)
    db.session.commit()

def create_bids():
    # Get all professionals
    all_professionals = User.query.filter_by(role=UserRole.PROFESSIONAL).all()
    
    for job in Job.query.filter(Job.status == JobStatus.OPEN).all():
        # Get the category and its subcategories
        category = Category.query.get(job.category_id)
        if not category:
            print(f"Job {job.id} has no valid category, skipping...")
            continue
            
        # Get all subcategory IDs (including the category itself if it has no parent)
        if category.parent_id is None:
            # This is a parent category, get all its subcategories
            subcategory_ids = [c.id for c in category.children]
        else:
            # This is already a subcategory
            subcategory_ids = [category.id]
            
        if not subcategory_ids:
            print(f"No subcategories found for job {job.id} in category {category.name}, skipping...")
            continue
            
        # Get all skills in these categories
        job_skills = Skill.query.filter(Skill.category_id.in_(subcategory_ids)).all()
        
        # Get professionals with matching skills
        matching_professionals = []
        if job_skills:
            matching_professionals = db.session.query(User).join(
                ProfessionalSkill, User.id == ProfessionalSkill.professional_id
            ).filter(
                ProfessionalSkill.skill_id.in_([s.id for s in job_skills]),
                User.role == UserRole.PROFESSIONAL
            ).distinct().all()
        
        # If no professionals with matching skills, use random professionals
        if not matching_professionals and all_professionals:
            print(f"No professionals with matching skills for job {job.id}, using random professionals")
            matching_professionals = random.sample(all_professionals, min(3, len(all_professionals)))
        
        # Determine number of bids to create (1-3, but no more than available professionals)
        num_bids = random.randint(1, min(3, len(matching_professionals)))
        
        # Create bids
        for _ in range(num_bids):
            if not matching_professionals:
                break
                
            professional = random.choice(matching_professionals)
            matching_professionals.remove(professional)
            
            # Convert Decimal to float for amount
            max_bid = float(job.budget)
            min_bid = max(100, max_bid * 0.5)  # Ensure minimum bid is reasonable
            
            # Create a reasonable bid amount (between 50% and 100% of job budget)
            bid_amount = round(random.uniform(min_bid, max_bid), 2)
            
            bid = Bid(
                job_id=job.id,
                professional_id=professional.id,
                amount=bid_amount,
                proposal=f"I can complete this job for ${bid_amount}. {fake.paragraph()}",
                timeline_weeks=random.randint(1, 12),
                status=BidStatus.PENDING,  # Start all as pending for testing
                created_at=fake.date_time_this_year()
            )
            db.session.add(bid)
            print(f"Created bid for job {job.id} by professional {professional.id} for ${bid_amount}")
    
    db.session.commit()
    print("Finished creating bids")

def create_reviews():
    completed_jobs = Job.query.filter_by(status=JobStatus.COMPLETED).all()
    for job in completed_jobs:
        accepted_bid = Bid.query.filter_by(job_id=job.id, status=BidStatus.ACCEPTED).first()
        if accepted_bid:
            review = Review(
                rating=random.randint(1, 5),
                comment=fake.paragraph(),
                job_id=job.id,
                professional_id=accepted_bid.professional_id,
                customer_id=job.customer_id,
                created_at=fake.date_time_this_year()
            )
            db.session.add(review)
    db.session.commit()

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
    with app.app_context():
        print("Dropping and recreating database tables...")
        db.drop_all()
        db.create_all()

        print("Creating categories and skills...")
        create_categories_and_skills()

        print("Creating users...")
        create_users()

        print("Assigning professional skills...")
        assign_professional_skills()

        print("Creating jobs...")
        create_jobs()

        print("Creating bids...")
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