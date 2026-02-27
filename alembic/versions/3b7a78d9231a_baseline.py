"""baseline

Revision ID: 3b7a78d9231a
Revises: d5ee48d0948a
Create Date: 2026-02-25 23:15:59.078153

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3b7a78d9231a'
down_revision: Union[str, Sequence[str], None] = 'd5ee48d0948a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
