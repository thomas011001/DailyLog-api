"""empty message

Revision ID: 709b160a5c14
Revises: b5727e8e2ae8
Create Date: 2026-03-20 04:18:12.146567

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "709b160a5c14"
down_revision: Union[str, Sequence[str], None] = "b5727e8e2ae8"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
