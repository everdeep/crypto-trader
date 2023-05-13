from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

from model.portfolio import PortfolioModel

Base = declarative_base()


class PortfolioHistoryModel(Base):
    __tablename__ = "portfolio_history"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    portfolio_id = Column(
        String(32), ForeignKey(PortfolioModel.id, ondelete="CASCADE"), nullable=False
    )
    total_earnings = Column(Float, nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return f"""
            PortfolioModel(
                id={self.id},
                portfolio_id={self.portfolio_id},
                total_earnings={self.total_earnings},
                created_at={self.created_at}
            )
        """
