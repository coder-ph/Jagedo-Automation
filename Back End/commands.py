import click
from flask import current_app
from flask.cli import with_appcontext
from models import db, User, UserRole, Category, Skill
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_app(app):
    """Register CLI commands with the Flask application."""
    app.cli.add_command(seed_db)

@click.command('seed-db')
@with_appcontext
def seed_db():
    """Seed the database with initial data."""
    click.echo('Starting database seeding...')
    
    # Create tables
    click.echo('Creating database tables...')
    db.create_all()
    
    # Create admin user
    click.echo('Creating admin user...')
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
        click.echo('Created admin user')
    
    # Create categories
    click.echo('Creating categories...')
    categories = [
        'Construction', 'Technology', 'Healthcare', 'Education',
        'Home Services', 'Automotive', 'Beauty & Wellness', 'Business Services'
    ]
    
    for name in categories:
        if not Category.query.filter_by(name=name).first():
            category = Category(name=name)
            db.session.add(category)
    
    db.session.commit()
    
    # Create skills
    click.echo('Creating skills...')
    skills_data = {
        'Construction': ['Carpentry', 'Masonry', 'Plumbing', 'Electrical', 'Painting'],
        'Technology': ['Web Development', 'Mobile Development', 'Data Science', 'UI/UX Design'],
        'Healthcare': ['Nursing', 'Physiotherapy', 'Nutrition', 'First Aid'],
    }
    
    for category_name, skill_names in skills_data.items():
        category = Category.query.filter_by(name=category_name).first()
        if category:
            for skill_name in skill_names:
                if not Skill.query.filter_by(name=skill_name).first():
                    skill = Skill(name=skill_name, category_id=category.id)
                    db.session.add(skill)
    
    db.session.commit()
    click.echo('Database seeding completed successfully!')
