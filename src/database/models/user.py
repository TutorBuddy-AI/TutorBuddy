from src.database import Base
from src.database.mixins import TimestampMixin
from sqlalchemy import (
    Column,
    String,
    Integer,
    ForeignKey,
    Boolean,
    Table,
    Unicode
)
from sqlalchemy.orm import relationship
from starlette.requests import Request
from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

user_roles = Table('user_roles', Base.metadata,
                   Column('user_id', ForeignKey('user.id')),
                   Column('role_id', ForeignKey('role.id'))
                   )


class Role(Base):
    __tablename__ = "role"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Unicode(255), nullable=False, unique=True)
    is_admin = Column(Boolean, default=False)

    users = relationship(
        "User",
        secondary=user_roles,
        back_populates="roles",
        lazy='joined')

    async def __admin_repr__(self, request: Request):
        return f"{self.name}"


class User(Base, TimestampMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, unique=True,
                index=True, autoincrement=True)
    tg_id = Column(String, unique=True)

    call_name = Column(String, nullable=False)
    email = Column(String, nullable=True, unique=True)
    speaker = Column(String, nullable=True, default="Anastasia")
    phone_number = Column(String, nullable=True)
    tg_firstName = Column(String, nullable=True)
    tg_lastName = Column(String, nullable=True)
    tg_language = Column(String, nullable=True)
    tg_username = Column(String, nullable=True)
    source = Column(String, nullable=True)

    goal = Column(String, nullable=True)
    native_lang = Column(String, nullable=True)
    teach_lang = Column(String, nullable=False, default="EN")
    topic = Column(String, nullable=True)
    additional_topic = Column(String, nullable=True)
    english_level = Column(String, nullable=True)
    time_zone = Column(String, nullable=True)

    roles = relationship(
        "Role",
        secondary=user_roles,
        back_populates="users",
        lazy='joined')
    
    # def verify_password(self, plain_password):
    #     return pwd_context.verify(plain_password, self.password)


    def get_password_hash(self, password):
        return pwd_context.hash(password)

    async def __admin_repr__(self, request: Request):
        return f"{self.email}"


class UserLocation(Base, TimestampMixin):
    __tablename__ = "user_location"

    id = Column(Integer, primary_key=True, unique=True,
                index=True, autoincrement=True)
    tg_id = Column(String, ForeignKey('user.tg_id'))

    ip_adress = Column(String, nullable=True)
    latitude = Column(String, nullable=True)
    longitude = Column(String, nullable=True)
    country_name = Column(String, nullable=True)
    country_code = Column(String, nullable=True)
    time_zone = Column(String, nullable=True)
    zip_code = Column(String, nullable=True)
    city_name = Column(String, nullable=True)
    region_name = Column(String, nullable=True)
    continent = Column(String, nullable=True)
    continent_code = Column(String, nullable=True)
