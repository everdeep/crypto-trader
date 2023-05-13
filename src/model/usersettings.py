from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

from model.user import UserModel

Base = declarative_base()


class UserSettingsModel(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer, ForeignKey(UserModel.id, ondelete="CASCADE"), nullable=False
    )
    key = Column(String(255), nullable=False)
    value = Column(String(255), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return f"""
            UserSettingsModel(
                id={self.id},
                user_id={self.user_id},
                key={self.key},
                value={self.value}
            )
        """
