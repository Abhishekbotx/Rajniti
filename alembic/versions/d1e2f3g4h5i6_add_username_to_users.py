"""add_username_to_users

Revision ID: d1e2f3g4h5i6
Revises: c1d2e3f4g5h6
Create Date: 2025-11-18 01:45:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from app.database.migration_utils import safe_add_column


# revision identifiers, used by Alembic.
revision: str = 'd1e2f3g4h5i6'
down_revision: Union[str, None] = 'c1d2e3f4g5h6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add username column to users table - idempotent migration."""
    # Add username column if it doesn't exist
    safe_add_column(
        'users',
        sa.Column('username', sa.String(), nullable=True)
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
