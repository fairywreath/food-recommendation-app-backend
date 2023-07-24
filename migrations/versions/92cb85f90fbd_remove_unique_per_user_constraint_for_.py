"""Remove unique per-user constraint for reviews

Revision ID: 92cb85f90fbd
Revises: 122007654f24
Create Date: 2023-07-24 07:56:41.470528

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '92cb85f90fbd'
down_revision = '122007654f24'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
