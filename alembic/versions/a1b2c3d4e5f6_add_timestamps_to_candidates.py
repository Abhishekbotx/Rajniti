"""add timestamps to candidates

Revision ID: a1b2c3d4e5f6
Revises: 93e1f7fdc7a0
Create Date: 2025-11-25 08:00:00.000000

"""
from typing import Sequence, Union
from datetime import datetime

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '93e1f7fdc7a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add created_at and updated_at columns to candidates table."""
    conn = op.get_bind()
    inspector = inspect(conn)
    columns = [c['name'] for c in inspector.get_columns('candidates')]
    
    # Add created_at column if it doesn't exist
    if 'created_at' not in columns:
        op.add_column(
            'candidates',
            sa.Column('created_at', sa.DateTime(), nullable=True)
        )
        # Set default value for existing rows
        op.execute("UPDATE candidates SET created_at = NOW() WHERE created_at IS NULL")
        # Make the column non-nullable after setting defaults
        op.alter_column('candidates', 'created_at', nullable=False)
    
    # Add updated_at column if it doesn't exist
    if 'updated_at' not in columns:
        op.add_column(
            'candidates',
            sa.Column('updated_at', sa.DateTime(), nullable=True)
        )
        # Set default value for existing rows
        op.execute("UPDATE candidates SET updated_at = NOW() WHERE updated_at IS NULL")
        # Make the column non-nullable after setting defaults
        op.alter_column('candidates', 'updated_at', nullable=False)


def downgrade() -> None:
    """Remove created_at and updated_at columns from candidates table."""
    conn = op.get_bind()
    inspector = inspect(conn)
    columns = [c['name'] for c in inspector.get_columns('candidates')]
    
    # Remove updated_at column if it exists
    if 'updated_at' in columns:
        op.drop_column('candidates', 'updated_at')
    
    # Remove created_at column if it exists
    if 'created_at' in columns:
        op.drop_column('candidates', 'created_at')

