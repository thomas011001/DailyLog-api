"""empty message

Revision ID: edd75f74dd91
Revises: 64f0c9ff8a17
Create Date: 2026-03-20 05:37:43.336755

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "edd75f74dd91"
down_revision: Union[str, Sequence[str], None] = "64f0c9ff8a17"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
