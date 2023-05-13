from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    String,
    Float,
    Boolean,
    DateTime,
    Enum,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

from enums import ExchangeType, OrderSide, OrderStatus, OrderType
from model.user import UserModel
from model.currencypairconfig import CurrencyPairConfigModel
from utils import get_uuid

Base = declarative_base()


class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(32), ForeignKey(UserModel.id), nullable=False)
    currency_pair = Column(String(20), nullable=False)
    order_id = Column(String(255), default=get_uuid, unique=True, nullable=False)
    bot_id = Column(Integer, ForeignKey(CurrencyPairConfigModel.id), nullable=True)
    exchange = Column(Enum(ExchangeType), nullable=False)
    cost = Column(Float, nullable=False)
    last_price = Column(Float, nullable=False)
    amount = Column(Float, nullable=False)
    side = Column(Enum(OrderSide), nullable=False)
    status = Column(Enum(OrderStatus), nullable=False)
    type = Column(Enum(OrderType), nullable=False)
    limit_price = Column(Float, nullable=True)
    is_autotraded = Column(Boolean, nullable=False)
    is_simulated = Column(Boolean, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return f"""
            OrderModel(
                id={self.id},
                user_id={self.user_id},
                currency_pair={self.currency_pair},
                order_id={self.order_id},
                exchange={self.exchange},
                cost={self.cost},
                last_price={self.last_price},
                amount={self.amount},
                side={self.side},
                status={self.status},
                type={self.type},
                limit_price={self.limit_price},
                is_autotraded={self.is_autotraded},
                is_simulated={self.is_simulated},
                created_at={self.created_at},
                updated_at={self.updated_at}
            )
        """
