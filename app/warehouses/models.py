from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.base import Base


class Warehouse(Base):
    __tablename__ = "warehouses"

    id: Mapped[int] = mapped_column(primary_key=True)
    inventory_id: Mapped[int] = mapped_column(ForeignKey("inventories.id"))
