from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.base import Base


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    warehouse_id: Mapped[int] = mapped_column(ForeignKey("warehouses.id"))
