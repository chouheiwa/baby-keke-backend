"""add_breast_side_for_simple_mode

添加 breast_side 字段用于支持快速记录模式（快速补记喂养）

Revision ID: 856b233987e8
Revises: 1f7d06ea70d1
Create Date: 2025-11-11 08:04:20.384548

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '856b233987e8'
down_revision: Union[str, None] = '1f7d06ea70d1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """添加 breast_side 字段"""
    # 添加 breast_side 字段用于快速记录模式
    op.add_column('feeding_records',
        sa.Column('breast_side',
                  sa.Enum('left', 'right', 'both', 'unknown', name='breast_side_enum'),
                  nullable=True,
                  comment='哺乳侧(用于快速记录模式)')
    )


def downgrade() -> None:
    """删除 breast_side 字段"""
    # 删除字段
    with op.batch_alter_table('feeding_records') as batch_op:
        batch_op.drop_column('breast_side')
