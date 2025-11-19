"""add_username_column_to_users

Revision ID: 8b6bb788ca7b
Revises: a1b2c3d4e5f6
Create Date: 2025-11-19 11:08:37.090416

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from app.database.migration_utils import safe_add_column


# revision identifiers, used by Alembic.
revision: str = '8b6bb788ca7b'
down_revision: Union[str, None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add username column to users table - idempotent migration."""
    # Add username column if it doesn't exist
    safe_add_column(
        'users',
        'username',
        sa.String(),
        nullable=True
    )
    
    # Create index for username if it doesn't exist
    try:
        op.create_index('ix_users_username', 'users', ['username'], unique=True)
    except Exception:
        # Index might already exist
        pass


def downgrade() -> None:
    """Remove username column from users table."""
    try:
        op.drop_index('ix_users_username', table_name='users')
    except Exception:
        pass
    
    try:
        op.drop_column('users', 'username')
    except Exception:
        pass
