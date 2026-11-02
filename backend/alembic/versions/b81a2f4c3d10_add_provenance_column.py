"""add_provenance_column

Revision ID: b81a2f4c3d10
Revises: 99a7aa6aeadd
Create Date: 2026-11-02 21:35:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b81a2f4c3d10'
down_revision: Union[str, Sequence[str], None] = '99a7aa6aeadd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    with op.batch_alter_table('claim_assessments', schema=None) as batch_op:
        batch_op.add_column(sa.Column('provenance', sa.String(length=50), nullable=True, server_default='OFFLINE_DETERMINISTIC'))


def downgrade() -> None:
    """Downgrade schema."""
    with op.batch_alter_table('claim_assessments', schema=None) as batch_op:
        batch_op.drop_column('provenance')

