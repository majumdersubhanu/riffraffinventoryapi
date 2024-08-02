from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.base import Base


class Inventory(Base):
    __tablename__ = "inventories"

    id: Mapped[int] = mapped_column(primary_key=True)
    shop_id: Mapped[int] = mapped_column(ForeignKey("shops.id"))
