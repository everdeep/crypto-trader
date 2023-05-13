from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

from model.portfolio import PortfolioModel

Base = declarative_base()


class BalanceModel(Base):
    __tablename__ = "balances"

    id = Column(Integer, primary_key=True)
    portfolio_id = Column(
        Integer, ForeignKey(PortfolioModel.id, ondelete="CASCADE"), nullable=False
    )
    asset = Column(String(10), nullable=False)
    free = Column(Float, nullable=False)
    locked = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return f"""
            BalanceModel(
                id={self.id},
                portfolio_id={self.portfolio_id},
                asset={self.asset},
                free={self.free},
                locked={self.locked},
                total={self.total},
                updated_at={self.updated_at}
            )
        """
