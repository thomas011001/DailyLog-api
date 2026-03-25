"""empty message

Revision ID: 10e5f1bd64b0
Revises: 2a89a8bb445e
Create Date: 2026-03-20 18:31:02.336441

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "10e5f1bd64b0"
down_revision: Union[str, Sequence[str], None] = "2a89a8bb445e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
