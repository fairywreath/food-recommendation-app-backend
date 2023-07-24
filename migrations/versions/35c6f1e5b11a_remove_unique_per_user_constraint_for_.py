"""Remove unique per-user constraint for reviews

Revision ID: 35c6f1e5b11a
Revises: 92cb85f90fbd
Create Date: 2023-07-24 07:57:44.880433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35c6f1e5b11a'
down_revision = '92cb85f90fbd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
