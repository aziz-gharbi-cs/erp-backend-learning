from decimal import Decimal

from pydantic import BaseModel, Field


class EmployeeCreateRequest(BaseModel):
    name: str = Field(..., min_length=1)
    job_title: str | None = None
    monthly_salary: Decimal | None = None


class EmployeeUpdateRequest(BaseModel):
    name: str | None = None
    job_title: str | None = None
    monthly_salary: Decimal | None = None


class EmployeeResponse(BaseModel):
    id: int
    name: str
    job_title: str | None = None
    monthly_salary: Decimal | None = None
