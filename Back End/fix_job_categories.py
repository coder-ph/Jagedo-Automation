from app import app, db
from models import Job, Category

def fix_job_categories():
    with app.app_context():
        # Get all jobs
        jobs = Job.query.all()
        
        # Get all child categories (subcategories)
        child_categories = Category.query.filter(Category.parent_id.isnot(None)).all()
        
        print(f"Found {len(jobs)} total jobs")
        print(f"Found {len(child_categories)} child categories")
        
        fixed_count = 0
        
        for job in jobs:
            category = Category.query.get(job.category_id)
            if category and category.parent_id is None:
                # This job is in a parent category, move it to a random child category
                if child_categories:
                    new_category = random.choice(child_categories)
                    print(f"Moving job {job.id} from parent category '{category.name}' to subcategory '{new_category.name}'")
                    job.category_id = new_category.id
                    fixed_count += 1
        
        if fixed_count > 0:
            db.session.commit()
            print(f"Fixed {fixed_count} jobs by moving them to subcategories")
        else:
            print("No jobs needed to be fixed")

if __name__ == "__main__":
    import random
    fix_job_categories()
