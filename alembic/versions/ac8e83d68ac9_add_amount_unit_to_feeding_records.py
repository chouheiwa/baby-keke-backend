"""add amount_unit to feeding_records

Revision ID: ac8e83d68ac9
Revises: 33b75965dcf7
Create Date: 2026-01-16 08:17:23.518028

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'ac8e83d68ac9'
down_revision: Union[str, None] = '33b75965dcf7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 只添加 amount_unit 字段到 feeding_records 表
    op.add_column('feeding_records', sa.Column('amount_unit', sa.String(length=20), nullable=True, comment='食量单位(如: g, ml, 滴, 勺, 碗等)'))


def downgrade() -> None:
    # 删除 amount_unit 字段
    op.drop_column('feeding_records', 'amount_unit')
