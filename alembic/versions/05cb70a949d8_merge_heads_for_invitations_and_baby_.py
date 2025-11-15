"""merge heads for invitations and baby extras

Revision ID: 05cb70a949d8
Revises: 7d3a1d8f2e90, a1b2c3d4e5f6
Create Date: 2025-11-14 22:28:12.566274

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05cb70a949d8'
down_revision: Union[str, None] = ('7d3a1d8f2e90', 'a1b2c3d4e5f6')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
