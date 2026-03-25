"""empty message

Revision ID: 819a0e78470b
Revises: 01d9d04e4416
Create Date: 2026-03-23 03:54:01.765746

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "819a0e78470b"
down_revision: Union[str, Sequence[str], None] = "01d9d04e4416"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
