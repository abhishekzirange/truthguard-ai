"""add_execution_mode_to_verification_runs

Revision ID: c19d3e5f7a20
Revises: b81a2f4c3d10
Create Date: 2026-11-02 22:05:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c19d3e5f7a20'
down_revision: Union[str, Sequence[str], None] = 'b81a2f4c3d10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('verification_runs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('execution_mode', sa.String(length=50), nullable=True, server_default='OFFLINE'))
        batch_op.add_column(sa.Column('integration_status', sa.JSON(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('verification_runs', schema=None) as batch_op:
        batch_op.drop_column('integration_status')
        batch_op.drop_column('execution_mode')

