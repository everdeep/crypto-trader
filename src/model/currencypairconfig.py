from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    Float,
    DateTime,
    Enum,
)
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

from enums import ExchangeType, Interval, StrategyType
from model.user import UserModel

Base = declarative_base()


class CurrencyPairConfigModel(Base):
    __tablename__ = "currency_pair_configs"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        String(32), ForeignKey(UserModel.id, ondelete="CASCADE"), nullable=False
    )
    currency_pair = Column(String(20))
    bot_name = Column(String(255), nullable=False)
    exchange = Column(Enum(ExchangeType), nullable=False)
    interval = Column(Enum(Interval), nullable=False)
    strategy = Column(Enum(StrategyType), nullable=False)
    limit = Column(Integer, nullable=False, default=1000)
    stop_loss = Column(Float, nullable=True)
    take_profit = Column(Float, nullable=True)
    earnings = Column(Float, nullable=False, default=0.0)
    allocated_balance = Column(Float, nullable=False, default=0.0)
    currency_free = Column(Float, nullable=False, default=0.0)
    currency_locked = Column(Float, nullable=False, default=0.0)
    asset_free = Column(Float, nullable=False, default=0.0)
    asset_locked = Column(Float, nullable=False, default=0.0)
    is_active = Column(Boolean, nullable=False, default=False)
    is_decommissioned = Column(Boolean, nullable=False, default=False)
    is_simulated = Column(Boolean, nullable=False, default=True)
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    # signal = db.relationship("SignalModel", backref="currency_pair_configs", cascade="all, delete")
    # orders = db.relationship("OrderModel", backref="currency_pair_configs")
    # strategy_config = db.relationship("StrategyConfigModel", backref="currency_pair_configs", cascade="all, delete")

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return f"""
            CurrencyPairConfig(
                id={self.id},
                user_id={self.user_id},
                currency_pair={self.currency_pair},
                exchange={self.exchange},
                interval={self.interval},
                strategy={self.strategy},
                limit={self.limit},
                stop_loss={self.stop_loss},
                take_profit={self.take_profit},
                earnings={self.earnings},
                allocated_balance={self.allocated_balance},
                currency_free={self.currency_free},
                currency_locked={self.currency_locked},
                asset_free={self.asset_free},
                asset_locked={self.asset_locked},
                is_active={self.is_active},
                is_decommissioned={self.is_decommissioned},
                is_simulated={self.is_simulated},
                updated_at={self.updated_at}

                signal={self.signal},
                orders={self.orders},
                strategy_config={self.strategy_config},
            )
        """
