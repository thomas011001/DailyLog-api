"""empty message

Revision ID: 088d1d317285
Revises: 10e5f1bd64b0
Create Date: 2026-03-20 18:32:41.651405

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "088d1d317285"
down_revision: Union[str, Sequence[str], None] = "10e5f1bd64b0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
