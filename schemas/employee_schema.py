from decimal import Decimal

from pydantic import BaseModel, Field

from models.employee import EmployeeRole


class EmployeeCreateRequest(BaseModel):
    name: str = Field(..., min_length=1)
    username: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)
    job_title: str | None = None
    monthly_salary: Decimal | None = None
    is_active: bool = True
    role: EmployeeRole = EmployeeRole.EMPLOYEE


class EmployeeUpdateRequest(BaseModel):
    name: str | None = None
    username: str | None = None
    password: str | None = None
    job_title: str | None = None
    monthly_salary: Decimal | None = None
    is_active: bool | None = None
    role: EmployeeRole | None = None


class EmployeeResponse(BaseModel):
    id: int
    name: str
    username: str
    job_title: str | None = None
    monthly_salary: Decimal | None = None
    is_active: bool
    role: EmployeeRole
