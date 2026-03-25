"""empty message

Revision ID: 4bb31fa5db4f
Revises: e09c932f8e9d
Create Date: 2026-03-20 04:14:15.282716

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "4bb31fa5db4f"
down_revision: Union[str, Sequence[str], None] = "e09c932f8e9d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
