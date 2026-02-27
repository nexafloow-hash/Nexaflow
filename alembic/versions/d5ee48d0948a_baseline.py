"""baseline

Revision ID: d5ee48d0948a
Revises: 1573a7ea7200
Create Date: 2026-02-25 23:12:50.722763

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd5ee48d0948a'
down_revision: Union[str, Sequence[str], None] = '1573a7ea7200'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
