"""Make from_status nullable in project_status_history

Revision ID: 123456789def
Revises: 2e104d35a4a3
Create Date: 2023-11-10 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '123456789def'
down_revision = '2e104d35a4a3'
branch_labels = None
depends_on = None

def upgrade():
    # Alter the column to be nullable
    with op.batch_alter_table('project_status_history') as batch_op:
        batch_op.alter_column('from_status', nullable=True)

def downgrade():
    # Before making it non-nullable, ensure there are no NULL values
    op.execute("UPDATE project_status_history SET from_status = 'open' WHERE from_status IS NULL")
    with op.batch_alter_table('project_status_history') as batch_op:
        batch_op.alter_column('from_status', nullable=False)
