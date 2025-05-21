import os
import json
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

    def handle_new_bid(self, bid_id):
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
                    # Evaluate project synchronously
                    self.evaluate_project(project.id)

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
                print(f"\n=== Starting evaluation for project {project_id} ===")
                project = Job.query.get(project_id)
                if not project:
                    error_msg = f"Project {project_id} not found for evaluation"
                    app.logger.error(error_msg)
                    print(error_msg)
                    return

                print(f"Project status: {project.status}")
                if project.status != JobStatus.OPEN:
                    info_msg = f"Project {project_id} is no longer open for bidding (status: {project.status})"
                    app.logger.info(info_msg)
                    print(info_msg)
                    return

                bids = Bid.query.filter_by(job_id=project_id, status=BidStatus.PENDING).all()
                print(f"Found {len(bids)} pending bids for project {project_id}")
                
                if not bids:
                    info_msg = f"No pending bids found for project {project_id}"
                    app.logger.info(info_msg)
                    print(info_msg)
                    await self.notify_admin_no_bids(project)
                    return

                print("\nScoring bids:")
                scored_bids = []
                for bid in bids:
                    score = self.calculate_bid_score(bid, project)
                    scored_bids.append((bid, score))
                    print(f"- Bid {bid.id}: Amount={bid.amount}, Timeline={bid.timeline_weeks}w, Score={score:.2f}, Bidder={bid.professional.name if bid.professional else 'None'}")
                
                scored_bids.sort(key=lambda x: x[1], reverse=True)
                best_bid, best_score = scored_bids[0] if scored_bids else (None, 0)
                
                print(f"\nBest bid: ID={best_bid.id if best_bid else 'None'}, Score={best_score:.2f}, Min Winning Score={self.min_winning_score}")

                if best_bid and best_score >= self.min_winning_score:
                    print(f"Accepting bid {best_bid.id} with score {best_score:.2f}")
                    await self.accept_bid(best_bid, best_score)
                else:
                    reason = "No bids meet minimum score" if best_bid else "No valid bids found"
                    print(f"No bid accepted. Reason: {reason}")
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
            
            amount_score = float(((project.budget - bid.amount) / project.budget) * 20)
            score += amount_score
        
       
        if hasattr(project, 'max_timeline') and project.max_timeline and bid.timeline_weeks <= project.max_timeline:
            
            timeline_score = ((project.max_timeline - bid.timeline_weeks) / project.max_timeline) * 10
            score += timeline_score
        
        
        return max(0, min(100, score))

    async def accept_bid(self, bid, score):
        print(f"\n=== Starting accept_bid for bid {bid.id} ===")
        print(f"Bid details: ID={bid.id}, Amount={bid.amount}, Bidder ID={bid.professional_id}")
        print(f"Project: ID={bid.job.id}, Title='{bid.job.title}', Status={bid.job.status}")
        
        with app.app_context():
            try:
                # Start a new transaction
                db.session.begin()
                
                # Get fresh instances to avoid detached instance issues
                fresh_bid = db.session.query(Bid).get(bid.id)
                project = db.session.query(Job).get(bid.job.id)
                
                if not fresh_bid or not project:
                    raise ValueError("Bid or Project not found in database")
                
                print("Updating bid status to ACCEPTED...")
                fresh_bid.status = BidStatus.ACCEPTED
                
                print(f"Updating project status to AWARDED and assigning contractor {fresh_bid.professional_id}...")
                project.status = JobStatus.AWARDED
                project.assigned_contractor_id = fresh_bid.professional_id
                
                print("Creating notifications...")
                # Convert Decimal to float for JSON serialization
                bid_amount = float(fresh_bid.amount) if hasattr(fresh_bid, 'amount') else 0.0
                
                # Get professional name from the bid's relationship or fall back to a query
                if fresh_bid.professional:
                    professional_name = fresh_bid.professional.name
                else:
                    # Fallback to query if relationship is not loaded
                    professional = db.session.get(User, fresh_bid.professional_id)
                    professional_name = professional.name if professional else "Unknown"
                
                # Notification for the contractor
                contractor_notification = Notification(
                    user_id=fresh_bid.professional_id,
                    title="Bid Accepted",
                    message=f"Your bid for project '{project.title}' has been accepted!",
                    content=json.dumps({
                        "project_id": project.id,
                        "project_title": project.title,
                        "bid_amount": bid_amount,
                        "score": float(score) if score is not None else 0.0,
                        "timestamp": datetime.utcnow().isoformat()
                    }, default=str),
                    notification_type="bid_accepted"
                )
                db.session.add(contractor_notification)
                print(f"Created contractor notification for user {fresh_bid.professional_id}")
                
                # Notification for the customer
                customer_notification = Notification(
                    user_id=project.customer_id,
                    title="Contractor Selected",
                    message=f"A contractor has been selected for your project '{project.title}'",
                    content=json.dumps({
                        "project_id": project.id,
                        "project_title": project.title,
                        "contractor_name": professional_name,
                        "contractor_id": fresh_bid.professional_id,
                        "bid_amount": bid_amount,
                        "score": float(score) if score is not None else 0.0,
                        "timestamp": datetime.utcnow().isoformat()
                    }, default=str),
                    notification_type="contractor_selected"
                )
                db.session.add(customer_notification)
                print(f"Created customer notification for user {project.customer_id}")
                
                print("Committing transaction...")
                db.session.commit()
                print("Transaction committed successfully!")
                
                # Refresh the bid and project to ensure we have the latest data
                db.session.refresh(fresh_bid)
                db.session.refresh(project)
                
                log_msg = f" Successfully accepted bid {fresh_bid.id} (${fresh_bid.amount}) for project {project.id} with score {score}"
                app.logger.info(log_msg)
                print(log_msg)
                print(f"Bid status after commit: {fresh_bid.status}")
                print(f"Project status after commit: {project.status}")
                print(f"Project assigned contractor after commit: {project.assigned_contractor_id}")
                
                return True
                
            except Exception as e:
                db.session.rollback()
                error_msg = f" Error accepting bid {bid.id}: {str(e)}"
                app.logger.error(error_msg)
                app.logger.exception("Full traceback:")
                print(error_msg)
                print("Transaction rolled back due to error")
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
                        notification_type="admin_action_required",
                        content=json.dumps({
                            "project_id": project.id,
                            "best_bid_id": best_bid.id if best_bid else None,
                            "best_score": best_score,
                            "action_required": "manual_review"
                        })
                    )
                    db.session.add(notification)
                
                db.session.commit()
                app.logger.info(f"Notified admin about project {project.id} needing manual review")
                
            except Exception as e:
                db.session.rollback()
                app.logger.error(f"Error notifying admin about manual review: {str(e)}")
                app.logger.exception("Full traceback:")
