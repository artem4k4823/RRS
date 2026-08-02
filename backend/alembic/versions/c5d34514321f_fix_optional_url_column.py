"""fix optional url column

Revision ID: c5d34514321f
Revises: 74a613b778e9
Create Date: 2026-08-02 07:15:14.602710

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c5d34514321f'
down_revision: Union[str, Sequence[str], None] = '74a613b778e9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
   
    op.create_table('optional-urls-list',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=128), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('description', sa.String(length=256), nullable=False),
    sa.Column('raiting', sa.Float(), server_default='0', nullable=False),
    sa.Column('likes', sa.Integer(), server_default='0', nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('id')
    )
   


def downgrade() -> None:
    """Downgrade schema."""
    
    op.drop_table('optional-urls-list')
   