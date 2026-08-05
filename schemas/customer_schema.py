from decimal import Decimal

from pydantic import BaseModel, Field


class CustomerCreateRequest(BaseModel):
    name: str = Field(..., min_length=1)
    phone: str = Field(..., min_length=1)
    email: str | None = None
    address: str | None = None
    tax_registration_number: str | None = None


class CustomerUpdateRequest(BaseModel):
    name: str | None = None
    phone: str | None = None
    email: str | None = None
    address: str | None = None
    tax_registration_number: str | None = None


class CustomerResponse(BaseModel):
    id: int
    name: str
    phone: str
    email: str | None = None
    address: str | None = None
    tax_registration_number: str | None = None
