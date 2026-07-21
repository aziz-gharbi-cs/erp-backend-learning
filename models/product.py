from decimal import Decimal

from sqlalchemy import Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.database import Base


class Product(Base):
    __tablename__ = "products"

    # ---------- Primary Key ----------

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    # ---------- Business Identity ----------

    reference: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )

    # ---------- Product Information ----------

    name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    # ---------- Pricing ----------

    unit_price_excl_tax: Mapped[Decimal] = mapped_column(
        Numeric(12, 3),
        nullable=False,
    )

    tax_rate: Mapped[Decimal] = mapped_column(
        Numeric(5, 2),
        nullable=False,
        default=Decimal("0.00"),
    )

    # ---------- Inventory ----------

    stock_quantity: Mapped[int] = mapped_column(
        nullable=False,
        default=0,
    )

    # ---------- Relationships ----------

    sale_lines: Mapped[list["SaleLine"]] = relationship(
        back_populates="product",
    )

    def __str__(self):
        return (
            f"Product("
            f"id={self.id}, "
            f"reference='{self.reference}', "
            f"name='{self.name}', "
            f"price={self.unit_price_excl_tax}, "
            f"stock={self.stock_quantity}"
            f")"
        )