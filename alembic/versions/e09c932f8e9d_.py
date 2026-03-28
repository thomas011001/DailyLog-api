"""empty message

Revision ID: e09c932f8e9d
Revises: 3ad92e5fe81e
Create Date: 2026-03-20 04:12:58.280364

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "e09c932f8e9d"
down_revision: Union[str, Sequence[str], None] = "3ad92e5fe81e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
