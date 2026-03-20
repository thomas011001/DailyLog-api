"""add timeblock and steps models

Revision ID: 3ad92e5fe81e
Revises: 5d6572a0f0cf
Create Date: 2026-03-20 04:06:32.323528

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "3ad92e5fe81e"
down_revision: Union[str, Sequence[str], None] = "5d6572a0f0cf"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
