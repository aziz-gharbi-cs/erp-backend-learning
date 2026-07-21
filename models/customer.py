from __future__ import annotations
from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base

from sqlalchemy import String

if TYPE_CHECKING:
    from models.invoice import Invoice
class Customer(Base):
    __tablename__ = "customers"

    # ---------- Primary Key ----------

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    # ---------- Customer Information ----------

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(
        String(300),
        nullable=True,
    )
    phone_number: Mapped[str | None] = mapped_column(
    String(20),
    nullable=True
    )

    tax_registration_number: Mapped[str | None] = mapped_column(
        String(50),
        unique=True,
        nullable=True,
    )

    # ---------- Relationships ----------

    invoices: Mapped[list["Invoice"]] = relationship(
        back_populates="customer",
    )

    def __str__(self):
        return (
            f"Customer("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"phone='{self.phone}'"
            f")"
        )