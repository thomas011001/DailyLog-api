"""empty message

Revision ID: 8ae589ab6aef
Revises: 709b160a5c14
Create Date: 2026-03-20 04:21:07.241514

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "8ae589ab6aef"
down_revision: Union[str, Sequence[str], None] = "709b160a5c14"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
