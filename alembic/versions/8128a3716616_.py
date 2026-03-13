"""empty message

Revision ID: 8128a3716616
Revises: a55a2511c7a0
Create Date: 2026-03-13 23:50:43.779045

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8128a3716616'
down_revision: Union[str, Sequence[str], None] = 'a55a2511c7a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
