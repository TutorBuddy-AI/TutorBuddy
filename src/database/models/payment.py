from sqlalchemy import Column, Integer, String, Unicode, Boolean, Date, DateTime
from src.database import Base
from src.database.mixins import TimestampMixin


class Subscription(Base, TimestampMixin):
    __tablename__ = "subscription"

    id = Column(Integer, primary_key=True)
    tg_id = Column(String, nullable=False)
    product_id = Column(String, nullable=False)
    count_msg = Column(Integer, nullable=True)
    count_mist = Column(Integer, nullable=True)
    start_at = Column(DateTime(timezone=True), nullable=False)
    end_at = Column(DateTime(timezone=True), nullable=False)


class Order(Base, TimestampMixin):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, unique=True,
                index=True, autoincrement=True)
    tg_id = Column(String, nullable=False)
    product_id = Column(String, nullable=False)
    product = Column(String, nullable=False)
    provider = Column(String, nullable=False)
    payment_id = Column(String, nullable=False)
    account_id = Column(String, nullable=True)
    gateway_id = Column(String, nullable=True)
    test = Column(Boolean, default=True)
    amount = Column(String, nullable=True)
    currency = Column(String, nullable=True)
    status = Column(String, nullable=True)
#    created_at = Column(DateTime(timezone=True), nullable=False, default=func.now())
    paid_at = Column(DateTime(timezone=True), nullable=True)