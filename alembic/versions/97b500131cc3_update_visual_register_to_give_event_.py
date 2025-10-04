"""Update visual register to give event status

Revision ID: 97b500131cc3
Revises: 32d22359768e
Create Date: 2025-10-04 14:39:57.246302

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97b500131cc3'
down_revision: Union[str, Sequence[str], None] = '32d22359768e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_column('visual_registers', 'is_processed')
    op.add_column('visual_registers', sa.Column('process_status', sa.Integer(), 
                                                nullable=False, default=0))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('visual_registers', 'process_status')
    op.add_column('visual_registers', sa.Column('is_processed', sa.Boolean(), 
                                                nullable=False, default=False))
    pass
