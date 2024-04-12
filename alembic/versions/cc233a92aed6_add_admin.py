"""Add admin

Revision ID: cc233a92aed6
Revises: 94e381370664
Create Date: 2024-04-07 19:39:12.634458

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_file

from sqlalchemy import orm

from database.models import Admin

# revision identifiers, used by Alembic.
revision = 'cc233a92aed6'
down_revision = '94e381370664'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    session.add(Admin(username="admin", password=Admin.get_password_hash("testpass")))
    session.commit()


def downgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    session.query(Admin).filter(Admin.username == "admin").delete()
    session.commit()
