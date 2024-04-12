"""Add admin

Revision ID: f3b54192f376
Revises: 05927834daa0
Create Date: 2024-04-12 21:33:30.768054

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_file
from sqlalchemy import orm

from database.models import Admin

# revision identifiers, used by Alembic.
revision = 'f3b54192f376'
down_revision = '05927834daa0'
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
