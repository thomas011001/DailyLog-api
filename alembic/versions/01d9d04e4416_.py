"""empty message

Revision ID: 01d9d04e4416
Revises: 789eded8cb86
Create Date: 2026-03-23 03:53:44.885056

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "01d9d04e4416"
down_revision: Union[str, Sequence[str], None] = "789eded8cb86"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
