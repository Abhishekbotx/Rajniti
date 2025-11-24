"""add_pincode_to_users

Revision ID: 20decf6f42ff
Revises: 8f1a2b3c4d5e
Create Date: 2025-11-24 10:28:26.312720

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = '20decf6f42ff'
down_revision: Union[str, None] = '8f1a2b3c4d5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add pincode column to users table if it doesn't exist."""
    conn = op.get_bind()
    inspector = inspect(conn)
    columns = [c['name'] for c in inspector.get_columns('users')]
    
    # Add pincode column if it doesn't exist
    if 'pincode' not in columns:
        op.add_column('users', sa.Column('pincode', sa.String(), nullable=True))


def downgrade() -> None:
    """Remove pincode column from users table."""
    conn = op.get_bind()
    inspector = inspect(conn)
    columns = [c['name'] for c in inspector.get_columns('users')]
    
    # Remove pincode column if it exists
    if 'pincode' in columns:
        op.drop_column('users', 'pincode')
