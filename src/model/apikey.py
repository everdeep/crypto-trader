from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import declarative_base

from enums import ExchangeType
from model.user import UserModel

Base = declarative_base()


class ApiKeyModel(Base):
    __tablename__ = "api_keys"

    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(
        String(32), ForeignKey(UserModel.id, ondelete="CASCADE"), nullable=False
    )
    exchange = Column(Enum(ExchangeType), nullable=False)
    api_key = Column(String(255), nullable=False)
    api_secret = Column(String(255), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return f"""
            ApiKeyModel(
                id={self.id},
                user_id={self.user_id},
                exchange={self.exchange},
                api_key={self.api_key},
                api_secret={self.api_secret}
            )
        """
