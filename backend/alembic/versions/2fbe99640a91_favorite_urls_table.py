"""favorite_urls_table

Revision ID: 2fbe99640a91
Revises: c5d34514321f
Create Date: 2026-08-09 05:40:00.454104

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2fbe99640a91'
down_revision: Union[str, Sequence[str], None] = 'c5d34514321f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.create_table('favorite_urls',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('url_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['url_id'], ['optional-urls-list.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id', 'url_id', name='uq_user_favorite_url')
    )
    op.create_index(op.f('ix_favorite_urls_id'), 'favorite_urls', ['id'], unique=False)
    op.create_index(op.f('ix_favorite_urls_user_id'), 'favorite_urls', ['user_id'], unique=False)
    op.create_unique_constraint(None, 'optional-urls-list', ['id'])



def downgrade() -> None:
    """Downgrade schema."""
  
    op.drop_constraint(None, 'optional-urls-list', type_='unique')
    op.drop_index(op.f('ix_favorite_urls_user_id'), table_name='favorite_urls')
    op.drop_index(op.f('ix_favorite_urls_id'), table_name='favorite_urls')
    op.drop_table('favorite_urls')
  
