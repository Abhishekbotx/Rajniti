"""add username to users

Revision ID: d7e8f9g0h1i2
Revises: c1d2e3f4g5h6
Create Date: 2025-11-18 04:24:46

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd7e8f9g0h1i2'
down_revision = 'c1d2e3f4g5h6'
branch_labels = None
depends_on = None


def upgrade():
    """Add username column to users table."""
    # Add username column
    op.add_column('users', sa.Column('username', sa.String(), nullable=True))
    
    # Add unique constraint and index
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)


def downgrade():
    """Remove username column from users table."""
    # Remove index and column
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_column('users', 'username')
