from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

from model.currencypairconfig import CurrencyPairConfigModel
from enums import Signal

Base = declarative_base()


class SignalModel(Base):
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True)
    currency_pair_config_id = Column(
        Integer,
        ForeignKey(CurrencyPairConfigModel.id, ondelete="CASCADE"),
        nullable=False,
    )
    signal = Column(Enum(Signal), nullable=False)
    last_trade_time = Column(DateTime, nullable=False)
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return f"""
            SignalModel(
                id={self.id},
                currency_pair_config_id={self.currency_pair_config_id},
                signal={self.signal},
                last_trade_time={self.last_trade_time},
                updated_at={self.updated_at}
            )
        """
