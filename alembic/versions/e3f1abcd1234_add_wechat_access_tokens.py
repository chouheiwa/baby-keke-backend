from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e3f1abcd1234'
down_revision: Union[str, None] = '05cb70a949d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'wechat_access_tokens',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column('appid', sa.String(length=64), nullable=False),
        sa.Column('token', sa.String(length=512), nullable=False),
        sa.Column('expires_at', sa.TIMESTAMP(), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        mysql_engine='InnoDB',
        mysql_default_charset='utf8mb4',
        mysql_collate='utf8mb4_unicode_ci',
    )
    op.create_unique_constraint('uk_wechat_appid', 'wechat_access_tokens', ['appid'])


def downgrade() -> None:
    op.drop_constraint('uk_wechat_appid', 'wechat_access_tokens', type_='unique')
    op.drop_table('wechat_access_tokens')