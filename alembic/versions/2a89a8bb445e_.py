"""empty message

Revision ID: 2a89a8bb445e
Revises: e2f9d65af31b
Create Date: 2026-03-20 18:06:03.556193

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "2a89a8bb445e"
down_revision: Union[str, Sequence[str], None] = "e2f9d65af31b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
