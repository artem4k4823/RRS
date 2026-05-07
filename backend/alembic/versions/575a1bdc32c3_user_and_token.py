"""User and token

Revision ID: 575a1bdc32c3
Revises: cf955a30a341
Create Date: 2026-05-07 14:19:59.971216

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '575a1bdc32c3'
down_revision: Union[str, Sequence[str], None] = 'cf955a30a341'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.create_table('users',
    sa.Column('username', sa.String(length=25), nullable=False),
    sa.Column('password', sa.String(length=20), nullable=False),
    sa.Column('isCreator', sa.Boolean(), server_default='0', nullable=False),
    sa.Column('isAdmin', sa.Boolean(), server_default='0', nullable=False),
    sa.Column('status', sa.Boolean(), server_default='1', nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('tokens',
    sa.Column('acces_token', sa.String(), nullable=False),
    sa.Column('expire_at', sa.DateTime(), nullable=False),
    sa.Column('refresh_token', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tokens_id'), 'tokens', ['id'], unique=False)
   


def downgrade() -> None:
    """Downgrade schema."""
    
    op.drop_index(op.f('ix_tokens_id'), table_name='tokens')
    op.drop_table('tokens')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
   
