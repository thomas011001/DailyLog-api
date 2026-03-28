"""empty message

Revision ID: 64f0c9ff8a17
Revises: 8ae589ab6aef
Create Date: 2026-03-20 05:36:30.229443

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "64f0c9ff8a17"
down_revision: Union[str, Sequence[str], None] = "8ae589ab6aef"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
