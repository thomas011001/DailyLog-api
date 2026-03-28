"""empty message

Revision ID: 789eded8cb86
Revises: 1d69858b6408
Create Date: 2026-03-21 20:54:39.451343

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "789eded8cb86"
down_revision: Union[str, Sequence[str], None] = "1d69858b6408"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
