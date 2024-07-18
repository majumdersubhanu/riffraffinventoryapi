from sqlalchemy import Column, Integer, String, DateTime, func, Boolean
from app.db import Base


class UserModel(Base):
    __tablename__ = "user_accounts"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    role = Column(String, index=True)
    organization = Column(String, index=True)
    createdAt = Column(DateTime, default=func.now())
    updatedAt = Column(DateTime, default=func.now(), onupdate=func.now())
    isActive = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"<User(id={self.id} username={self.username} role={self.role} organization={self.organization} isActive={self.isActive})>"