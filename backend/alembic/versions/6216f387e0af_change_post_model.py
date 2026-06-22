"""change post model

Revision ID: 6216f387e0af
Revises: 43631ca06b1c
Create Date: 2026-06-15 16:43:55.392323

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6216f387e0af'
down_revision: Union[str, Sequence[str], None] = '43631ca06b1c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
   
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=500), nullable=False),
    sa.Column('link', sa.String(length=1000), nullable=False),
    sa.Column('summary', sa.Text(), nullable=True),
    sa.Column('published_at', sa.DateTime(), nullable=True),
    sa.Column('feed_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('is_read', sa.Boolean(), nullable=False),
    sa.Column('is_favorite', sa.Boolean(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['feed_id'], ['subscriptions.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_posts_id'), 'posts', ['id'], unique=False)
    op.create_index(op.f('ix_posts_link'), 'posts', ['link'], unique=True)
    op.create_index(op.f('ix_posts_published_at'), 'posts', ['published_at'], unique=False)
  


def downgrade() -> None:
    """Downgrade schema."""
    
    op.drop_index(op.f('ix_posts_published_at'), table_name='posts')
    op.drop_index(op.f('ix_posts_link'), table_name='posts')
    op.drop_index(op.f('ix_posts_id'), table_name='posts')
    op.drop_table('posts')
   
