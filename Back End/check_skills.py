from app import app, db
from models import Skill, ProfessionalSkill, Job, Category, User, Bid

def check_skills():
    with app.app_context():
        
        print("=== Categories and Skills ===")
        for category in Category.query.all():
            print(f"\nCategory: {category.name} (ID: {category.id})")
            if category.children:
                print("  Subcategories:")
                for child in category.children:
                    print(f"  - {child.name} (ID: {child.id})")
            skills = Skill.query.filter_by(category_id=category.id).all()
            if skills:
                print("  Skills:")
                for skill in skills:
                    print(f"  - {skill.name} (ID: {skill.id})")
        
        
        print("\n=== All Professionals and Their Skills ===")
        professionals = User.query.filter_by(role='professional').all()
        for prof in professionals:
            print(f"\nProfessional: {prof.name} (ID: {prof.id})")
            skills = db.session.query(Skill).join(
                ProfessionalSkill, 
                Skill.id == ProfessionalSkill.skill_id
            ).filter(
                ProfessionalSkill.professional_id == prof.id
            ).all()
            if skills:
                for skill in skills:
                    print(f"  - {skill.name} (Category ID: {skill.category_id})")
            else:
                print("  No skills assigned")
        
        
        print("\n=== Open Jobs and Potential Matches ===")
        open_jobs = Job.query.filter_by(status='open').all()
        for job in open_jobs:
            category = Category.query.get(job.category_id)
            print(f"\nJob: {job.title} (ID: {job.id})")
            print(f"Category: {category.name if category else 'None'} (ID: {job.category_id})")
            
            
            if category:
                if category.parent_id is None:
                    
                    subcategories = [c.id for c in category.children]
                else:
                    subcategories = [category.id]
                
                relevant_skills = Skill.query.filter(
                    Skill.category_id.in_(subcategories)
                ).all()
                
                
                matching_pros = db.session.query(User).join(
                    ProfessionalSkill,
                    User.id == ProfessionalSkill.professional_id
                ).filter(
                    ProfessionalSkill.skill_id.in_([s.id for s in relevant_skills]),
                    User.role == 'professional'
                ).distinct().all()
                
                print(f"  Potential matching professionals: {len(matching_pros)}")
                for pro in matching_pros[:3]:  # Show first 3 matches
                    print(f"  - {pro.name} (ID: {pro.id})")
                if len(matching_pros) > 3:
                    print(f"  ... and {len(matching_pros) - 3} more")
            else:
                print("  No category assigned to this job")

if __name__ == "__main__":
    check_skills()
