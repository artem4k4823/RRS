"""add refresh token remove access

Revision ID: b60d2b7ea788
Revises: 38cd59dbee64
Create Date: 2026-06-12 14:56:35.728252

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b60d2b7ea788'
down_revision: Union[str, Sequence[str], None] = '38cd59dbee64'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
   
    op.create_table('refresh_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('expire_at', sa.DateTime(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('token')
    )
    op.create_index(op.f('ix_refresh_tokens_id'), 'refresh_tokens', ['id'], unique=False)
    op.drop_index(op.f('ix_tokens_id'), table_name='tokens')
    op.drop_table('tokens')
   


def downgrade() -> None:
    """Downgrade schema."""
    
    op.create_table('tokens',
    sa.Column('acces_token', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('expire_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=False),
    sa.Column('refresh_token', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name=op.f('tokens_user_id_fkey'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('tokens_pkey'))
    )
    op.create_index(op.f('ix_tokens_id'), 'tokens', ['id'], unique=False)
    op.drop_index(op.f('ix_refresh_tokens_id'), table_name='refresh_tokens')
    op.drop_table('refresh_tokens')
   
