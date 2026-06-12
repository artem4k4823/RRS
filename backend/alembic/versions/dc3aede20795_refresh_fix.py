"""refresh fix

Revision ID: dc3aede20795
Revises: b60d2b7ea788
Create Date: 2026-06-12 15:32:26.107242

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc3aede20795'
down_revision: Union[str, Sequence[str], None] = 'b60d2b7ea788'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
   
    op.add_column('refresh_tokens', sa.Column('user_username', sa.String(), nullable=False))
    op.drop_column('refresh_tokens', 'user_id')
    


def downgrade() -> None:
    """Downgrade schema."""
   
    op.add_column('refresh_tokens', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('refresh_tokens', 'user_username')
   
