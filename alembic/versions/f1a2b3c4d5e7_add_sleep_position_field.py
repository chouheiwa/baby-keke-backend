"""add_sleep_position_field

添加 position 字段用于记录睡眠姿势（左/中/右）

Revision ID: f1a2b3c4d5e7
Revises: 856b233987e8
Create Date: 2025-11-15 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1a2b3c4d5e7'
down_revision: Union[str, None] = '856b233987e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """添加 position 字段"""
    op.add_column(
        'sleep_records',
        sa.Column(
            'position',
            sa.Enum('left', 'middle', 'right', name='sleep_position_enum'),
            nullable=True,
            comment='睡眠姿势(左/中/右)'
        )
    )


def downgrade() -> None:
    """删除 position 字段"""
    with op.batch_alter_table('sleep_records') as batch_op:
        batch_op.drop_column('position')