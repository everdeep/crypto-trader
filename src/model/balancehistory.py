from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

from model.balance import BalanceModel

Base = declarative_base()


class BalanceHistoryModel(Base):
    __tablename__ = "balance_history"

    id = Column(Integer, primary_key=True)
    balance_id = Column(
        Integer, ForeignKey(BalanceModel.id, ondelete="CASCADE"), nullable=False
    )
    asset = Column(String(10), nullable=False)
    free = Column(Float, nullable=False)
    locked = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return f"""
            BalanceModel(
                id={self.id},
                balance_id={self.balance_id},
                asset={self.asset},
                free={self.free},
                locked={self.locked},
                total={self.total},
                created_at={self.created_at}
            )
        """
