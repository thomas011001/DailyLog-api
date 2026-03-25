"""empty message

Revision ID: 1d69858b6408
Revises: 088d1d317285
Create Date: 2026-03-20 18:33:44.600845

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "1d69858b6408"
down_revision: Union[str, Sequence[str], None] = "088d1d317285"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
