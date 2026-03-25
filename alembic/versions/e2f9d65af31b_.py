"""empty message

Revision ID: e2f9d65af31b
Revises: edd75f74dd91
Create Date: 2026-03-20 18:03:49.929047

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "e2f9d65af31b"
down_revision: Union[str, Sequence[str], None] = "edd75f74dd91"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
