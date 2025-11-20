"""add_users_table

Revision ID: c1d2e3f4g5h6
Revises: 2b1da9ee1f5d
Create Date: 2025-11-17 18:15:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.database.migration_utils import safe_add_column, table_exists


# revision identifiers, used by Alembic.
revision: str = 'c1d2e3f4g5h6'
down_revision: Union[str, None] = '2b1da9ee1f5d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Create users table - idempotent migration."""
    # Only create table if it doesn't exist
    if not table_exists('users'):
        op.create_table(
            'users',
            sa.Column('id', sa.String(), nullable=False),
            sa.Column('email', sa.String(), nullable=False),
            sa.Column('name', sa.String(), nullable=True),
            sa.Column('profile_picture', sa.String(), nullable=True),
            sa.Column('phone', sa.String(), nullable=True),
            sa.Column('state', sa.String(), nullable=True),
            sa.Column('city', sa.String(), nullable=True),
            sa.Column('age_group', sa.String(), nullable=True),
            sa.Column('political_interest', sa.String(), nullable=True),
            sa.Column('preferred_parties', sa.Text(), nullable=True),
            sa.Column('topics_of_interest', sa.Text(), nullable=True),
            sa.Column('onboarding_completed', sa.Boolean(), nullable=False, server_default='false'),
            sa.Column('created_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
            sa.Column('updated_at', sa.DateTime(), nullable=False, server_default=sa.text('CURRENT_TIMESTAMP')),
            sa.Column('last_login', sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email')
        )
        
        # Create indexes
        op.create_index('ix_users_id', 'users', ['id'], unique=False)
        op.create_index('ix_users_email', 'users', ['email'], unique=True)


def downgrade() -> None:
    """Drop users table - idempotent."""
    if table_exists('users'):
        op.drop_index('ix_users_email', table_name='users')
        op.drop_index('ix_users_id', table_name='users')
        op.drop_table('users')
