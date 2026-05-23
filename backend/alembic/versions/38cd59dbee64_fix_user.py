"""fix user

Revision ID: 38cd59dbee64
Revises: 575a1bdc32c3
Create Date: 2026-05-23 20:19:42.316193

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '38cd59dbee64'
down_revision: Union[str, Sequence[str], None] = '575a1bdc32c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.alter_column('users', 'password',
               existing_type=sa.VARCHAR(length=20),
               type_=sa.String(length=128),
               existing_nullable=False)
    


def downgrade() -> None:
    """Downgrade schema."""

    op.alter_column('users', 'password',
               existing_type=sa.String(length=128),
               type_=sa.VARCHAR(length=20),
               existing_nullable=False)
   
