"""add column is_revoked

Revision ID: e041591407df
Revises: dc3aede20795
Create Date: 2026-06-12 17:42:21.488584

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e041591407df'
down_revision: Union[str, Sequence[str], None] = 'dc3aede20795'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.add_column('refresh_tokens', sa.Column('is_revoked', sa.Boolean(), nullable=False))
    


def downgrade() -> None:
    """Downgrade schema."""
   
    op.drop_column('refresh_tokens', 'is_revoked')
    
