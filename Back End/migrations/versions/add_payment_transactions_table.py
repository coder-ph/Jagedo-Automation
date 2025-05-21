"""Add payment transactions table

Revision ID: 123456789012
Revises: 123456789def
Create Date: 2025-05-21 20:40:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision = '123456789012'
down_revision = '123456789def'
branch_labels = None
depends_on = None

def upgrade():
    # Create enum types first
    payment_status = sa.Enum(
        'pending', 'completed', 'failed', 'cancelled', 'refunded',
        name='payment_status'
    )
    payment_method = sa.Enum(
        'mpesa', 'card', 'bank_transfer', 'paypal', 'other',
        name='payment_method'
    )
    
    # Create the payment_transactions table
    op.create_table(
        'payment_transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Integer(), nullable=True),
        sa.Column('amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('currency', sa.String(3), nullable=False, default='KES'),
        sa.Column('status', payment_status, nullable=False, default='pending'),
        sa.Column('method', payment_method, nullable=True),
        sa.Column('reference', sa.String(100), nullable=False, unique=True),
        sa.Column('mpesa_receipt', sa.String(50), nullable=True),
        sa.Column('phone_number', sa.String(20), nullable=True),
        sa.Column('metadata', JSONB, nullable=True, default={}),
        sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP'), onupdate=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['project_id'], ['jobs.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Create indexes
    op.create_index(op.f('ix_payment_transactions_reference'), 'payment_transactions', ['reference'], unique=True)
    op.create_index(op.f('ix_payment_transactions_user_id'), 'payment_transactions', ['user_id'], unique=False)
    op.create_index(op.f('ix_payment_transactions_project_id'), 'payment_transactions', ['project_id'], unique=False)
    op.create_index(op.f('ix_payment_transactions_status'), 'payment_transactions', ['status'], unique=False)
    op.create_index(op.f('ix_payment_transactions_created_at'), 'payment_transactions', ['created_at'], unique=False)

def downgrade():
    # Drop indexes first
    op.drop_index(op.f('ix_payment_transactions_created_at'), table_name='payment_transactions')
    op.drop_index(op.f('ix_payment_transactions_status'), table_name='payment_transactions')
    op.drop_index(op.f('ix_payment_transactions_project_id'), table_name='payment_transactions')
    op.drop_index(op.f('ix_payment_transactions_user_id'), table_name='payment_transactions')
    op.drop_index(op.f('ix_payment_transactions_reference'), table_name='payment_transactions')
    
    # Drop the table
    op.drop_table('payment_transactions')
    
    # Drop enum types
    sa.Enum(name='payment_status').drop(op.get_bind(), checkfirst=False)
    sa.Enum(name='payment_method').drop(op.get_bind(), checkfirst=False)
