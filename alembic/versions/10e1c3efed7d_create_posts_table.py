"""create posts table

Revision ID: 10e1c3efed7d
Revises: 
Create Date: 2025-07-20 20:25:24.840681

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10e1c3efed7d'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
