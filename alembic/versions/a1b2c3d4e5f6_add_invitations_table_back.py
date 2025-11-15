from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, None] = '1f7d06ea70d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if 'invitations' in inspector.get_table_names():
        return

    op.create_table(
        'invitations',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('baby_id', sa.Integer(), sa.ForeignKey('babies.id', ondelete='CASCADE'), nullable=False),
        sa.Column('invite_code', sa.String(length=64), nullable=False),
        sa.Column('created_by', sa.Integer(), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('expire_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('status', sa.Enum('active', 'expired', 'used', name='invitation_status_enum'), nullable=False, server_default=sa.text("'active'")),
        sa.Column('used_by', sa.Integer(), sa.ForeignKey('users.id'), nullable=True),
        sa.Column('used_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        mysql_engine='InnoDB',
        mysql_default_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci',
    )
    op.create_index('uk_invite_code', 'invitations', ['invite_code'], unique=True)
    op.create_index('idx_baby_id', 'invitations', ['baby_id'], unique=False)
    op.create_index('idx_status_expire', 'invitations', ['status', 'expire_at'], unique=False)
    op.create_index('idx_created_by', 'invitations', ['created_by'], unique=False)


def downgrade() -> None:
    op.drop_index('idx_created_by', table_name='invitations')
    op.drop_index('idx_status_expire', table_name='invitations')
    op.drop_index('idx_baby_id', table_name='invitations')
    op.drop_index('uk_invite_code', table_name='invitations')
    op.drop_table('invitations')