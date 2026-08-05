from decimal import Decimal

from pydantic import BaseModel, Field


class ProductCreateRequest(BaseModel):
    reference: str = Field(..., min_length=1)
    name: str = Field(..., min_length=1)
    description: str | None = None
    unit_price_excl_tax: Decimal
    tax_rate: Decimal = Decimal("0.00")
    stock_quantity: int = 0


class ProductUpdateRequest(BaseModel):
    reference: str | None = None
    name: str | None = None
    description: str | None = None
    unit_price_excl_tax: Decimal | None = None
    tax_rate: Decimal | None = None
    stock_quantity: int | None = None


class ProductResponse(BaseModel):
    id: int
    reference: str
    name: str
    description: str | None = None
    unit_price_excl_tax: Decimal
    tax_rate: Decimal
    stock_quantity: int
