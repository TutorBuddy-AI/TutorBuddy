"""Added Ekaterinas person

Revision ID: 60a8aa8169de
Revises: 4de1582836c9
Create Date: 2024-05-12 17:26:59.498996

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_file
from sqlalchemy import orm

from database.models import Person

# revision identifiers, used by Alembic.
revision = '60a8aa8169de'
down_revision = '4de1582836c9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    session.add(Person(id="Katya", short_name="Katya", full_name="Ekaterina"))
    session.commit()


def downgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    session.query(Person).filter(Person.id == "Katya").delete()
    session.commit()
