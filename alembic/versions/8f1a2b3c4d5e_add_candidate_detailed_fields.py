"""add candidate detailed fields

Revision ID: 8f1a2b3c4d5e
Revises: 
Create Date: 2025-11-21 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8f1a2b3c4d5e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add new columns to candidates table
    op.add_column('candidates', sa.Column('political_background', sa.JSON(), nullable=True))
    op.add_column('candidates', sa.Column('liabilities', sa.JSON(), nullable=True))
    op.add_column('candidates', sa.Column('crime_cases', sa.JSON(), nullable=True))


def downgrade() -> None:
    # Remove columns from candidates table
    op.drop_column('candidates', 'crime_cases')
    op.drop_column('candidates', 'liabilities')
    op.drop_column('candidates', 'political_background')

