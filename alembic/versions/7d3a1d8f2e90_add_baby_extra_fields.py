"""add_baby_extra_fields

Revision ID: 7d3a1d8f2e90
Revises: 856b233987e8
Create Date: 2025-11-11 14:22:00

为 babies 表增加 nickname, birth_weight, birth_height 字段
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d3a1d8f2e90'
down_revision: Union[str, None] = '856b233987e8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'babies',
        sa.Column(
            'nickname',
            sa.String(length=100),
            nullable=True,
            comment='宝宝昵称',
        ),
    )
    op.add_column(
        'babies',
        sa.Column(
            'birth_weight',
            sa.Integer(),
            nullable=True,
            comment='出生体重(g)',
        ),
    )
    op.add_column(
        'babies',
        sa.Column(
            'birth_height',
            sa.Integer(),
            nullable=True,
            comment='出生身长(cm)',
        ),
    )


def downgrade() -> None:
    op.drop_column('babies', 'birth_height')
    op.drop_column('babies', 'birth_weight')
    op.drop_column('babies', 'nickname')