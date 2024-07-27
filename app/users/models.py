from sqlalchemy.orm import Mapped, mapped_column
from app.base import Base
from app.utils.user_roles_enum import UserRoles


class User(Base):
    __tablename__ = "user_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(index=True)
    password: Mapped[str] = mapped_column()

    f_name: Mapped[str] = mapped_column(nullable=True)
    l_name: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(index=True)

    role: Mapped[UserRoles] = mapped_column(default=UserRoles.ADMIN)

    def __repr__(self) -> str:
        return f"<User(id={self.id} username={self.username} email={self.email} role={self.role}"
