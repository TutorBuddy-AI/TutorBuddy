"""merge user message mistakes, questions and feedback

Revision ID: c71b956d516b
Revises: 31139e0e4554, d091c2665d62
Create Date: 2023-12-14 00:57:35.190722

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c71b956d516b'
down_revision = ('31139e0e4554', 'd091c2665d62')
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
