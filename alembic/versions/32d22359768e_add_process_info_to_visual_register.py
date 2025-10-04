"""Add process info to visual register

Revision ID: 32d22359768e
Revises: 208688373b26
Create Date: 2025-10-04 12:18:14.687415

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '32d22359768e'
down_revision: Union[str, Sequence[str], None] = '208688373b26'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('visual_registers', sa.Column('is_processed', sa.Boolean(), 
                                                nullable=False, default=False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('visual_registers', 'is_processed')
    pass
