"""merge multiple heads

Revision ID: 43631ca06b1c
Revises: 39279f643929, e06791f594a2
Create Date: 2026-06-15 16:43:00.006497

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '43631ca06b1c'
down_revision: Union[str, Sequence[str], None] = ('39279f643929', 'e06791f594a2')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
