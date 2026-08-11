from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database.database import Base
from sqlalchemy.orm import relationship

from sqlalchemy import ForeignKey

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.employee import Employee
class User(Base):
    __tablename__ = "users"

    # ---------- Primary Key ----------

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    # ---------- Authentication ----------

    username: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # ---------- Personal Information ----------

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        unique=True,
    )

    phone_number: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    # ---------- Account Status ----------

    email_verified: Mapped[bool] = mapped_column(
        nullable=False,
        default=False,
    )

    role: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="USER",
    )

    is_active: Mapped[bool] = mapped_column(
        nullable=False,
        default=True,
    )
    employee_id: Mapped[int | None] = mapped_column(
    ForeignKey("employees.id"),
    nullable=True,
    unique=True,
    )   
    employee: Mapped["Employee | None"] = relationship(
    back_populates="user",
    uselist=False,
)
    def __str__(self):
        return (
            f"User("
            f"id={self.id}, "
            f"username='{self.username}', "
            f"name='{self.name}', "
            f"email='{self.email}', "
            f"role='{self.role}', "
            f"is_active={self.is_active}"
            f")"
        )