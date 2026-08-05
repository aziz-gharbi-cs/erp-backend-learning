from __future__ import annotations
from decimal import Decimal
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.invoice import Invoice
from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


class Employee(Base):
    __tablename__ = "employees"

    # ---------- Primary Key ----------

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    # ---------- Personal Information ----------

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    job_title: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # ---------- Payroll ----------

    monthly_salary: Mapped[Decimal] = mapped_column(
        Numeric(12, 3),
        nullable=False,
    )

    invoices: Mapped[list["Invoice"]] = relationship(
        back_populates="employee",
    )

    def __str__(self):
        return (
            f"Employee("
            f"id={self.id}, "
            f"name='{self.name}', "
            f"job_title='{self.job_title}'"
            f")"
        )