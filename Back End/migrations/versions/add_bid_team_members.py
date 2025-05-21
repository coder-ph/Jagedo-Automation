"""Add bid team members

Revision ID: 123456789abc
Revises: 
Create Date: 2025-05-21 15:20:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '123456789abc'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Create bid_team_members table
    op.create_table(
        'bid_team_members',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('bid_id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('role', sa.String(255), nullable=False),
        sa.Column('hourly_rate', sa.Numeric(10, 2), nullable=False),
        sa.Column('hours', sa.Float, nullable=False),
        sa.Column('total_cost', sa.Numeric(10, 2), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.ForeignKeyConstraint(['bid_id'], ['bids.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Add index for faster lookups by bid_id and email
    op.create_index('idx_bid_team_members_bid_id', 'bid_team_members', ['bid_id'])
    op.create_index('idx_bid_team_members_email', 'bid_team_members', ['email'])

def downgrade():
    op.drop_table('bid_team_members')
