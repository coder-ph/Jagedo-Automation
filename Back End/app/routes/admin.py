from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func, extract, case, and_
from datetime import datetime, timedelta
from ..models import db, User, Job, Bid, Review, Category, PaymentTransaction
from ..models.enums import UserRole, JobStatus, PaymentStatus
from functools import wraps

bp = Blueprint('admin', __name__, url_prefix='/api/admin')

def admin_required(f):
    @wraps(f)
    @jwt_required()
    def decorated_function(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        if not user or user.role != UserRole.ADMIN:
            return jsonify({"msg": "Admin access required"}), 403
        return f(*args, **kwargs)
    return decorated_function

@bp.route('/dashboard/stats', methods=['GET'])
@admin_required
def get_dashboard_stats():
    # User Statistics
    total_users = User.query.count()
    new_users_this_month = User.query.filter(
        extract('month', User.created_at) == datetime.utcnow().month,
        extract('year', User.created_at) == datetime.utcnow().year
    ).count()
    
    professionals = User.query.filter_by(role=UserRole.PROFESSIONAL).count()
    customers = total_users - professionals - 1  # Subtract admin
    
    # Job Statistics
    total_jobs = Job.query.count()
    active_jobs = Job.query.filter(Job.status.in_([JobStatus.OPEN, JobStatus.IN_PROGRESS])).count()
    completed_jobs = Job.query.filter_by(status=JobStatus.COMPLETED).count()
    
    # Revenue Statistics
    total_revenue = db.session.query(
        func.coalesce(func.sum(PaymentTransaction.amount), 0)
    ).filter(
        PaymentTransaction.status == PaymentStatus.COMPLETED
    ).scalar() or 0
    
    # Recent Jobs
    recent_jobs = Job.query.order_by(Job.created_at.desc()).limit(5).all()
    
    # Category Distribution
    category_stats = db.session.query(
        Category.name,
        func.count(Job.id).label('job_count')
    ).join(
        Job, Category.id == Job.category_id
    ).group_by(Category.name).all()
    
    # Monthly Stats
    monthly_stats = db.session.query(
        extract('month', Job.created_at).label('month'),
        extract('year', Job.created_at).label('year'),
        func.count(Job.id).label('job_count'),
        func.sum(case([(Job.status == JobStatus.COMPLETED, 1)], else_=0)).label('completed_jobs'),
        func.coalesce(
            func.sum(case([
                (and_(
                    PaymentTransaction.job_id.isnot(None),
                    PaymentTransaction.status == PaymentStatus.COMPLETED
                ), PaymentTransaction.amount)], 
                else_=0
            )), 0
        ).label('revenue')
    ).outerjoin(
        PaymentTransaction, Job.id == PaymentTransaction.job_id
    ).filter(
        Job.created_at >= datetime.utcnow() - timedelta(days=365)
    ).group_by(
        extract('year', Job.created_at),
        extract('month', Job.created_at)
    ).order_by(
        extract('year', Job.created_at).desc(),
        extract('month', Job.created_at).desc()
    ).limit(12).all()
    
    return jsonify({
        'user_stats': {
            'total_users': total_users,
            'new_users_this_month': new_users_this_month,
            'professionals': professionals,
            'customers': customers
        },
        'job_stats': {
            'total_jobs': total_jobs,
            'active_jobs': active_jobs,
            'completed_jobs': completed_jobs,
            'completion_rate': round((completed_jobs / total_jobs * 100), 2) if total_jobs > 0 else 0
        },
        'revenue_stats': {
            'total_revenue': float(total_revenue) if total_revenue else 0,
            'average_job_value': round(float(total_revenue) / total_jobs, 2) if total_jobs > 0 else 0
        },
        'category_distribution': [
            {'category': name, 'count': count} for name, count in category_stats
        ],
        'monthly_stats': [{
            'month': int(stat.month),
            'year': int(stat.year),
            'job_count': stat.job_count,
            'completed_jobs': stat.completed_jobs,
            'revenue': float(stat.revenue) if stat.revenue else 0
        } for stat in monthly_stats],
        'recent_jobs': [{
            'id': job.id,
            'title': job.title,
            'status': job.status.value,
            'created_at': job.created_at.isoformat(),
            'budget': float(job.budget) if job.budget else 0,
            'customer_name': job.customer.full_name if job.customer else 'N/A'
        } for job in recent_jobs]
    })
