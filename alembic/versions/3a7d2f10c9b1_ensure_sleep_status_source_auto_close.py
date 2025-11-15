"""ensure sleep status/source/auto_close columns exist

Revision ID: 3a7d2f10c9b1
Revises: 2c5f9e1a7b3d
Create Date: 2025-11-16 11:05:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3a7d2f10c9b1'
down_revision: Union[str, None] = '2c5f9e1a7b3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    insp = sa.inspect(bind)
    existing_cols = {col['name'] for col in insp.get_columns('sleep_records')}

    if 'status' not in existing_cols:
        op.add_column(
            'sleep_records',
            sa.Column(
                'status',
                sa.Enum('in_progress', 'completed', 'auto_closed', 'cancelled', name='sleep_status_enum'),
                nullable=False,
                server_default='completed'
            )
        )
        op.execute("UPDATE sleep_records SET status='completed' WHERE status IS NULL")

    if 'auto_closed_at' not in existing_cols:
        op.add_column('sleep_records', sa.Column('auto_closed_at', sa.TIMESTAMP(), nullable=True))

    if 'source' not in existing_cols:
        op.add_column(
            'sleep_records',
            sa.Column(
                'source',
                sa.Enum('manual', 'auto', name='sleep_source_enum'),
                nullable=False,
                server_default='manual'
            )
        )
        op.execute("UPDATE sleep_records SET source='manual' WHERE source IS NULL")


def downgrade() -> None:
    op.drop_column('sleep_records', 'source')
    op.drop_column('sleep_records', 'auto_closed_at')
    op.drop_column('sleep_records', 'status')