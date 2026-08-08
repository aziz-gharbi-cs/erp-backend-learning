from __future__ import annotations
from decimal import Decimal
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum as SAEnum, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base

if TYPE_CHECKING:
    from models.invoice import Invoice


class EmployeeRole(str, Enum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    EMPLOYEE = "EMPLOYEE"


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

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False,
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    role: Mapped[EmployeeRole] = mapped_column(
        SAEnum(EmployeeRole, native_enum=False),
        default=EmployeeRole.EMPLOYEE,
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
            f"username='{self.username}', "
            f"role='{self.role.value}'"
            f")"
        )