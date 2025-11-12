"""remove_redundant_feeding_fields

移除冗余的母乳喂养字段，简化为只使用 feeding_sequence

Revision ID: 1f7d06ea70d1
Revises: 18b5981b1793
Create Date:2025-11-10 22:55:08.808533

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f7d06ea70d1'
down_revision: Union[str, None] = '18b5981b1793'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """删除冗余字段"""
    # 删除 breast_side 字段
    with op.batch_alter_table('feeding_records') as batch_op:
        batch_op.drop_column('breast_side')
        batch_op.drop_column('duration_left')
        batch_op.drop_column('duration_right')


def downgrade() -> None:
    """恢复冗余字段（不建议使用）"""
    # 恢复字段
    op.add_column('feeding_records',
        sa.Column('breast_side', sa.Enum('left', 'right', 'both', name='breast_side_enum'), nullable=True, comment='哺乳侧')
    )
    op.add_column('feeding_records',
        sa.Column('duration_left', sa.Integer(), nullable=True, comment='左侧总时长(分钟)')
    )
    op.add_column('feeding_records',
        sa.Column('duration_right', sa.Integer(), nullable=True, comment='右侧总时长(分钟)')
    )
