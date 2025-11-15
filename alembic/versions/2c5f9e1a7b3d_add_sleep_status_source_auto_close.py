"""add sleep status/source/auto_close columns

Revision ID: 2c5f9e1a7b3d
Revises: 05cb70a949d8
Create Date: 2025-11-16 10:45:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c5f9e1a7b3d'
down_revision: Union[str, None] = '05cb70a949d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'sleep_records',
        sa.Column(
            'status',
            sa.Enum('in_progress', 'completed', 'auto_closed', 'cancelled', name='sleep_status_enum'),
            nullable=False,
            server_default='completed'
        )
    )

    op.add_column(
        'sleep_records',
        sa.Column('auto_closed_at', sa.TIMESTAMP(), nullable=True)
    )

    op.add_column(
        'sleep_records',
        sa.Column(
            'source',
            sa.Enum('manual', 'auto', name='sleep_source_enum'),
            nullable=False,
            server_default='manual'
        )
    )

    op.execute("UPDATE sleep_records SET status='completed' WHERE status IS NULL")
    op.execute("UPDATE sleep_records SET source='manual' WHERE source IS NULL")


def downgrade() -> None:
    op.drop_column('sleep_records', 'source')
    op.drop_column('sleep_records', 'auto_closed_at')
    op.drop_column('sleep_records', 'status')