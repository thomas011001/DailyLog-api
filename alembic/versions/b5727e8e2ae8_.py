"""empty message

Revision ID: b5727e8e2ae8
Revises: 4bb31fa5db4f
Create Date: 2026-03-20 04:18:07.490876

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "b5727e8e2ae8"
down_revision: Union[str, Sequence[str], None] = "4bb31fa5db4f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
