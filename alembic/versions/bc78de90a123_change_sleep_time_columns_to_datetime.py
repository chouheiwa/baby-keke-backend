"""change sleep time columns to datetime

Revision ID: bc78de90a123
Revises: ab12cd34ef56
Create Date: 2025-11-16 12:20:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bc78de90a123'
down_revision: Union[str, None] = 'ab12cd34ef56'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('sleep_records', 'start_time',
                    existing_type=sa.TIMESTAMP(),
                    type_=sa.DateTime(),
                    nullable=False)

    op.alter_column('sleep_records', 'end_time',
                    existing_type=sa.TIMESTAMP(),
                    type_=sa.DateTime(),
                    nullable=True)

    op.alter_column('sleep_records', 'auto_closed_at',
                    existing_type=sa.TIMESTAMP(),
                    type_=sa.DateTime(),
                    nullable=True)


def downgrade() -> None:
    op.alter_column('sleep_records', 'auto_closed_at',
                    existing_type=sa.DateTime(),
                    type_=sa.TIMESTAMP(),
                    nullable=True)

    op.alter_column('sleep_records', 'end_time',
                    existing_type=sa.DateTime(),
                    type_=sa.TIMESTAMP(),
                    nullable=True)

    op.alter_column('sleep_records', 'start_time',
                    existing_type=sa.DateTime(),
                    type_=sa.TIMESTAMP(),
                    nullable=False)