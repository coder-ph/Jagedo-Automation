"""merge heads

Revision ID: 2e104d35a4a3
Revises: 0386be2d6c2a, 123456789abc
Create Date: 2025-05-21 15:23:39.786217

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2e104d35a4a3'
down_revision = ('0386be2d6c2a', '123456789abc')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
