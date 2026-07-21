from __future__ import annotations
from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
if TYPE_CHECKING:
    from models.customer import Customer
    from models.employee import Employee
    from models.saleline import SaleLine
from database.database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    # ---------- Primary Key ----------

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    # ---------- Business Information ----------

    invoice_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    invoice_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    invoice_date: Mapped[date] = mapped_column(
        default=date.today,
        nullable=False,
    )

    # ---------- Foreign Keys ----------

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
    )

    employee_id: Mapped[int] = mapped_column(
        ForeignKey("employees.id"),
        nullable=False,
    )

    # ---------- Relationships ----------

    customer: Mapped["Customer"] = relationship(
        back_populates="invoices",
    )

    employee: Mapped["Employee"] = relationship(
        back_populates="invoices",
    )

    sale_lines: Mapped[list["SaleLine"]] = relationship(
        back_populates="invoice",
        cascade="all, delete-orphan",
    )

    def __str__(self):
        return (
            f"Invoice("
            f"id={self.id}, "
            f"invoice_number='{self.invoice_number}', "
            f"invoice_type='{self.invoice_type}', "
            f"status='{self.status}', "
            f"invoice_date={self.invoice_date}, "
            f"customer_id={self.customer_id}, "
            f"employee_id={self.employee_id}, "
            f"lines={len(self.sale_lines)}"
            f")"
        )