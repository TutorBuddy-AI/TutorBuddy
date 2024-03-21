"""made consistent person user reference

Revision ID: 9ebae0accd9e
Revises: 4d2f397e8ef6
Create Date: 2024-03-18 15:36:02.743849

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_file
from sqlalchemy.sql import insert
from sqlalchemy import orm

from database.models import Person

# revision identifiers, used by Alembic.
revision = '9ebae0accd9e'
down_revision = '4d2f397e8ef6'
branch_labels = None
depends_on = None

lookup_values = {
    "TutorBuddy": Person(id="TutorBuddy", short_name="TutorBuddy", full_name="TutorBuddy"),
    "Anastasia": Person(id="Anastasia", short_name="Anastasia", full_name="Anastasia Andrizh"),
    "Oksana": Person(id="Oksana", short_name="Oksana", full_name="Oksana Zakharova"),
    "AA_Lingua": Person(id="AA_Lingua", short_name="Anastasia", full_name="Anastasia Isakova")}


def upgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)

    session.add_all(lookup_values.values())
    session.commit()


def downgrade() -> None:
    bind = op.get_bind()
    session = orm.Session(bind=bind)
    # ToDo delete
