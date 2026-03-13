"""empty message

Revision ID: 2c181d894946
Revises: 8128a3716616
Create Date: 2026-03-13 23:54:01.934334

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2c181d894946'
down_revision: Union[str, Sequence[str], None] = '8128a3716616'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
