from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.base import Base


class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True, index=True)
    admin_id: Mapped[int] = mapped_column(ForeignKey("user_accounts.id"))
