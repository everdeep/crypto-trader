from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import declarative_base

from enums import StrategyType
from model.currencypairconfig import CurrencyPairConfigModel

Base = declarative_base()


class StrategyConfigModel(Base):
    __tablename__ = "strategy_configs"

    id = Column(Integer, primary_key=True, nullable=False)
    currency_pair_config_id = Column(
        Integer,
        ForeignKey(CurrencyPairConfigModel.id, ondelete="CASCADE"),
        nullable=False,
    )
    strategy = Column(Enum(StrategyType), nullable=False)
    key = Column(String(255), nullable=False)
    value = Column(Integer, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return f"""
            StrategyConfigModel(
                id={self.id},
                currency_pair_config_id={self.currency_pair_config_id},
                strategy={self.strategy},
                key={self.key},
                value={self.value}
            )
        """
