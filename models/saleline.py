from __future__ import annotations
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.database import Base


class SaleLine(Base):
    __tablename__ = "sale_lines"

    # ---------- Primary Key ----------

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    # ---------- Relationships ----------

    invoice_id: Mapped[int] = mapped_column(
        ForeignKey("invoices.id"),
        nullable=False,
    )

    product_id: Mapped[int | None] = mapped_column(
        ForeignKey("products.id"),
        nullable=True,
    )

    invoice: Mapped["Invoice"] = relationship(
        back_populates="sale_lines",
    )

    product: Mapped["Product | None"] = relationship(
        back_populates="sale_lines",
    )

    # ---------- Snapshot ----------

    product_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    product_description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    # ---------- Commercial ----------

    quantity: Mapped[int] = mapped_column(
        nullable=False,
    )

    unit_price_excl_tax: Mapped[Decimal] = mapped_column(
        Numeric(12, 3),
        nullable=False,
    )

    tax_rate: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
    )

    discount_rate: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        default=Decimal("0.00"),
        nullable=False,
    )

    @property
    def unit_price_incl_tax(self) -> Decimal:
        return self.unit_price_excl_tax * (
            Decimal("1") + self.tax_rate / Decimal("100")
        )

    @property
    def total_excl_tax(self) -> Decimal:
        total = self.unit_price_excl_tax * self.quantity
        total *= Decimal("1") - self.discount_rate / Decimal("100")
        return total

    @property
    def total_tax(self) -> Decimal:
        return self.total_incl_tax - self.total_excl_tax

    @property
    def total_incl_tax(self) -> Decimal:
        total = self.unit_price_incl_tax * self.quantity
        total *= Decimal("1") - self.discount_rate / Decimal("100")
        return total

    def __str__(self):
        return (
            f"SaleLine("
            f"id={self.id}, "
            f"product='{self.product_name}', "
            f"quantity={self.quantity}, "
            f"unit_price={self.unit_price_excl_tax}, "
            f"discount={self.discount_rate}%, "
            f"total={self.total_incl_tax}"
            f")"
        )