from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

from model.user import UserModel

Base = declarative_base()


class PortfolioModel(Base):
    __tablename__ = "portfolios"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id = Column(
        String(32), ForeignKey(UserModel.id, ondelete="CASCADE"), nullable=False
    )
    total_earnings = Column(Float, nullable=False, default=0.0)
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return f"""
            PortfolioModel(
                id={self.id},
                user_id={self.user_id},
                total_earnings={self.total_earnings},
                updated_at={self.updated_at},
            )
        """
