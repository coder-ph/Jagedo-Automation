from .base import BaseModel
from app import db

class Category(BaseModel):
    __tablename__ = 'categories'
    
    name = db.Column(db.String(255), unique=True, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    # Self-referential relationship for parent-child categories
    parent = db.relationship('Category', remote_side='Category.id', backref='children')
    
    def to_dict(self, include_children=False):
        result = {
            'id': self.id,
            'name': self.name,
            'parent_id': self.parent_id
        }
        
        if include_children and self.children:
            result['children'] = [child.to_dict(include_children=True) for child in self.children]
            
        return result


class Skill(BaseModel):
    __tablename__ = 'skills'
    
    name = db.Column(db.String(255), unique=True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category_id': self.category_id
        }


class ProfessionalSkill(BaseModel):
    __tablename__ = 'professional_skills'
    
    professional_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skills.id'), primary_key=True)
    certified = db.Column(db.Boolean, default=False)
    years_experience = db.Column(db.Integer)
    nca_ratings = db.Column(db.String(255))
    
    # Relationships
    skill = db.relationship('Skill')
    
    def to_dict(self):
        return {
            'professional_id': self.professional_id,
            'skill': self.skill.to_dict() if self.skill else None,
            'certified': self.certified,
            'years_experience': self.years_experience,
            'nca_ratings': self.nca_ratings
        }
