"""drop sleep_type column from sleep_records

Revision ID: ab12cd34ef56
Revises: 2c5f9e1a7b3d
Create Date: 2025-11-16 12:00:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab12cd34ef56'
down_revision: Union[str, None] = '2c5f9e1a7b3d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_column('sleep_records', 'sleep_type')


def downgrade() -> None:
    op.add_column(
        'sleep_records',
        sa.Column(
            'sleep_type',
            sa.Enum('night', 'nap', name='sleep_type_enum'),
            nullable=False
        )
    )