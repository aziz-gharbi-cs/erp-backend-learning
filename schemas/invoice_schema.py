from decimal import Decimal

from pydantic import BaseModel, Field


class SaleLineCreateRequest(BaseModel):
    product_id: int
    quantity: int
    discount_rate: Decimal | None = Decimal("0.00")


class InvoiceCreateRequest(BaseModel):
    customer_id: int
    employee_id: int
    invoice_number: str = Field(..., min_length=1)
    sale_lines: list[SaleLineCreateRequest]


class InvoiceResponse(BaseModel):
    id: int
    invoice_number: str
    invoice_type: str
    status: str
    invoice_date: str
    customer_id: int
    employee_id: int
