import os
import time
from datetime import datetime, timedelta
from sqlalchemy import and_
from models import db, Job, Bid, Notification, JobStatus, BidStatus, User, UserRole
from app import app
import threading
        

class BidAutomation:
    def __init__(self, min_bids=5, evaluation_period_hours=24):
       
        self.min_bids = min_bids
        self.evaluation_period = timedelta(hours=evaluation_period_hours)
        self.min_winning_score = 60  

    async def handle_new_bid(self, bid_id):
        
        with app.app_context():
            try:
                bid = Bid.query.get(bid_id)
                if not bid:
                    app.logger.error(f"Bid {bid_id} not found")
                    return

                project = Job.query.get(bid.job_id)
                if not project:
                    app.logger.error(f"Project {bid.job_id} not found for bid {bid_id}")
                    return
                
                if len(project.bids) == 1:
                    app.logger.info(f"First bid received for project {project.id}, scheduling evaluation")
                    
                    self.schedule_evaluation(project.id)
                

                if len(project.bids) >= self.min_bids:
                    await self.evaluate_project(project.id)

            except Exception as e:
                app.logger.error(f"Error in handle_new_bid: {str(e)}")
                app.logger.exception("Full traceback:")

    def schedule_evaluation(self, project_id):
       # use a task queue like Celery production environment
       
      
        def _evaluate_after_delay():
            time.sleep(self.evaluation_period.total_seconds())
            with app.app_context():
                self.evaluate_project(project_id)
        
        thread = threading.Thread(target=_evaluate_after_delay)
        thread.daemon = True
        thread.start()

    async def evaluate_project(self, project_id):
   
        with app.app_context():
            try:
                project = Job.query.get(project_id)
                if not project:
                    app.logger.error(f"Project {project_id} not found for evaluation")
                    return

                
                if project.status != JobStatus.OPEN:
                    app.logger.info(f"Project {project_id} is no longer open for bidding")
                    return

                bids = Bid.query.filter_by(job_id=project_id, status=BidStatus.PENDING).all()
                
                if not bids:
                    app.logger.info(f"No pending bids found for project {project_id}")
                    await self.notify_admin_no_bids(project)
                    return

                
                scored_bids = []
                for bid in bids:
                    score = self.calculate_bid_score(bid, project)
                    scored_bids.append((bid, score))
                
                
                scored_bids.sort(key=lambda x: x[1], reverse=True)
                best_bid, best_score = scored_bids[0] if scored_bids else (None, 0)

               
                if best_bid and best_score >= self.min_winning_score:
                    await self.accept_bid(best_bid, best_score)
                else:
                    await self.notify_admin_manual_review(project, best_bid, best_score)

            except Exception as e:
                app.logger.error(f"Error in evaluate_project: {str(e)}")
                app.logger.exception("Full traceback:")


    def calculate_bid_score(self, bid, project):
       
        score = 0.0
        
       
        contractor = bid.professional
        
       
        nca_score = (contractor.nca_level / 8) * 40
        score += nca_score
        
       
        rating_score = (contractor.average_rating / 5) * 30 if contractor.average_rating else 0
        score += rating_score
        
       
        if 0 < bid.amount <= project.budget:
            
            amount_score = ((project.budget - bid.amount) / project.budget) * 20
            score += amount_score
        
       
        if hasattr(project, 'max_timeline') and project.max_timeline and bid.timeline_weeks <= project.max_timeline:
            
            timeline_score = ((project.max_timeline - bid.timeline_weeks) / project.max_timeline) * 10
            score += timeline_score
        
        
        return max(0, min(100, score))

    async def accept_bid(self, bid, score):
       
        with app.app_context():
            try:
                
                bid.status = BidStatus.ACCEPTED
                
                
                project = bid.job
                project.status = JobStatus.AWARDED
                project.assigned_contractor_id = bid.professional_id
                
                
                notification = Notification(
                    user_id=bid.professional_id,
                    title="Bid Accepted",
                    message=f"Your bid for project '{project.title}' has been accepted!",
                    notification_type="bid_accepted"
                )
                db.session.add(notification)
                
                
                notification = Notification(
                    user_id=project.customer_id,
                    title="Contractor Selected",
                    message=f"A contractor has been selected for your project '{project.title}'",
                    notification_type="contractor_selected"
                )
                db.session.add(notification)
                
                db.session.commit()
                
                app.logger.info(f"Bid {bid.id} accepted for project {project.id} with score {score}")
                
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Error accepting bid {bid.id}: {str(e)}")
                app.logger.exception("Full traceback:")
                raise

    async def notify_admin_no_bids(self, project):
       
        with app.app_context():
            try:
                
                admins = User.query.filter_by(role=UserRole.ADMIN).all()
                
                for admin in admins:
                    notification = Notification(
                        user_id=admin.id,
                        title="Manual Assignment Required",
                        message=f"Project '{project.title}' received no bids. Manual assignment required.",
                        notification_type="admin_action_required"
                    )
                    db.session.add(notification)
                
                db.session.commit()
                app.logger.info(f"Notified admin about project {project.id} with no bids")
                
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Error notifying admin about no bids: {str(e)}")
                app.logger.exception("Full traceback:")

    async def notify_admin_manual_review(self, project, best_bid, best_score):
       
        with app.app_context():
            try:
                
                admins = User.query.filter_by(role=UserRole.ADMIN).all()
                
                for admin in admins:
                    message = (
                        f"Project '{project.title}' has bids but none meet the minimum score. "
                        f"Best bid score: {best_score:.1f}/100. "
                        f"Please review manually."
                    )
                    
                    notification = Notification(
                        user_id=admin.id,
                        title="Manual Review Required",
                        message=message,
                        notification_type="admin_action_required"
                    )
                    db.session.add(notification)
                
                db.session.commit()
                app.logger.info(f"Notified admin about project {project.id} needing manual review")
                
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Error notifying admin about manual review: {str(e)}")
                app.logger.exception("Full traceback:")
