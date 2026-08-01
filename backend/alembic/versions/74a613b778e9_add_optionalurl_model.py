"""add OptionalUrl model

Revision ID: 74a613b778e9
Revises: 6216f387e0af
Create Date: 2026-08-01 07:35:37.080239

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '74a613b778e9'
down_revision: Union[str, Sequence[str], None] = '6216f387e0af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
   
    op.drop_index(op.f('ix_posts_link'), table_name='posts')
    op.create_index(op.f('ix_posts_link'), 'posts', ['link'], unique=False)
    op.drop_constraint(op.f('users_username_key'), 'users', type_='unique')
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
   


def downgrade() -> None:
    """Downgrade schema."""
  
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.create_unique_constraint(op.f('users_username_key'), 'users', ['username'], postgresql_nulls_not_distinct=False)
    op.drop_index(op.f('ix_posts_link'), table_name='posts')
    op.create_index(op.f('ix_posts_link'), 'posts', ['link'], unique=True)
 