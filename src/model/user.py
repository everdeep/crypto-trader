from sqlalchemy import Column, Integer, String, Date, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

from uuid import uuid4

Base = declarative_base()


def get_uuid():
    return uuid4().hex


class UserModel(Base):
    __tablename__ = "users"

    id = Column(
        String(32), primary_key=True, default=get_uuid, unique=True, nullable=False
    )
    email = Column(String(255), nullable=False)
    _password = Column(String(128), nullable=False)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    username = Column(String(128), nullable=True)
    dob = Column(Date, nullable=True)
    phone = Column(String(64), nullable=True)
    is_admin = Column(Integer, nullable=False, default=0)
    is_active = Column(Integer, nullable=False, default=1)
    is_verified = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(
        DateTime, nullable=False, default=func.now(), onupdate=func.now()
    )

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self) -> str:
        return f"""
            UserModel(
                id={self.id},
                email={self.email},
                _password={self._password},
                first_name={self.first_name},
                last_name={self.last_name},
                username={self.username},
                dob={self.dob},
                phone={self.phone},
                is_admin={self.is_admin},
                is_active={self.is_active},
                is_verified={self.is_verified},
                created_at={self.created_at},
                updated_at={self.updated_at},
                settings={self.settings},
                address={self.address},
                portfolio={self.portfolio}
            )
        """
