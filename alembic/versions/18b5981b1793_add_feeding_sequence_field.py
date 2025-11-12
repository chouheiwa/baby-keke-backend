"""add_feeding_sequence_field

Revision ID: 18b5981b1793
Revises: 9be5093dbf84
Create Date: 2025-11-10 22:32:58.509568

添加 feeding_sequence 字段以支持母乳交替喂养记录
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '18b5981b1793'
down_revision: Union[str, None] = '9be5093dbf84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """添加 feeding_sequence 字段"""
    # 添加字段到 feeding_records 表
    op.add_column('feeding_records',
        sa.Column('feeding_sequence', sa.Text(), nullable=True, comment='喂养序列JSON(母乳交替记录)')
    )


def downgrade() -> None:
    """移除 feeding_sequence 字段"""
    # 删除字段
    op.drop_column('feeding_records', 'feeding_sequence')
