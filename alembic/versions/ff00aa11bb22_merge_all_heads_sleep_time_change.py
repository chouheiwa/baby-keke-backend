"""merge all heads including sleep time change

Revision ID: ff00aa11bb22
Revises: 3a7d2f10c9b1, bc78de90a123, e3f1abcd1234, f1a2b3c4d5e7
Create Date: 2025-11-16 12:28:00

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff00aa11bb22'
down_revision: Union[str, None] = ('3a7d2f10c9b1', 'bc78de90a123', 'e3f1abcd1234', 'f1a2b3c4d5e7')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass