from app import app, db
from models import User, Job, Skill, ProfessionalSkill, Category

def check_database():
    with app.app_context():
        print("=== Database Summary ===")
        print(f"Total Users: {User.query.count()}")
        print(f"Professionals: {User.query.filter_by(role='professional').count()}")
        print(f"Customers: {User.query.filter_by(role='customer').count()}")
        print(f"Admins: {User.query.filter_by(role='admin').count()}")
        print(f"\nTotal Jobs: {Job.query.count()}")
        print(f"Open Jobs: {Job.query.filter_by(status='open').count()}")
        print(f"\nTotal Skills: {Skill.query.count()}")
        print(f"Professional Skills: {ProfessionalSkill.query.count()}")
        print(f"\nCategories: {Category.query.count()}")
        
        # Print first few users
        print("\n=== Sample Users ===")
        for user in User.query.limit(3).all():
            print(f"ID: {user.id}, Email: {user.email}, Role: {user.role}")
        
        # Print first few jobs
        print("\n=== Sample Jobs ===")
        for job in Job.query.limit(3).all():
            print(f"ID: {job.id}, Title: {job.title}, Status: {job.status}, Category ID: {job.category_id}")

if __name__ == "__main__":
    check_database()
