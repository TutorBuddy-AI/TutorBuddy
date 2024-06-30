"""Added Victorias person

Revision ID: 4de1582836c9
Revises: 6df4ad791d58
Create Date: 2024-05-06 22:36:23.905855

"""
from alembic import op
from sqlalchemy import orm

from database.models import Person

# revision identifiers, used by Alembic.
revision = '4de1582836c9'
down_revision = '6df4ad791d58'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    session.add(Person(id="Victoria", short_name="Victoria", full_name="Victoria"))
    session.commit()


def downgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    session.query(Person).filter(Person.id == "Victoria").delete()
    session.commit()
