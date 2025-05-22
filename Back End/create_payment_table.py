from app import create_app
from app.extensions import db
from app.models.payment import PaymentTransaction, PaymentStatus, PaymentMethod
from sqlalchemy import inspect

def create_payment_table():
    """Create the payment_transactions table if it doesn't exist."""
    app = create_app('development')
    with app.app_context():
        # Create the table if it doesn't exist
        inspector = inspect(db.engine)
        if 'payment_transactions' not in inspector.get_table_names():
            PaymentTransaction.__table__.create(db.engine)
            print("Created payment_transactions table")
        else:
            print("payment_transactions table already exists")

if __name__ == '__main__':
    create_payment_table()
