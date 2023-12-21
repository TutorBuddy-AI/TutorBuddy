"""Merge news and hints

Revision ID: 8b44c2f62f63
Revises: 0f2a0514f4ea, d7a287c1a749
Create Date: 2023-12-20 01:31:11.814021

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8b44c2f62f63'
down_revision = ('0f2a0514f4ea', 'd7a287c1a749')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
