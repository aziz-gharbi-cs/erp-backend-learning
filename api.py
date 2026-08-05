from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Any

from database.database import Base, SessionLocal, engine, get_db
from models.customer import Customer
from models.employee import Employee
from models.product import Product
from models.invoice import Invoice
from services.customer_service import CustomerService
from services.employee_service import EmployeeService
from services.product_service import ProductService
from services.invoice_service import InvoiceService

Base.metadata.create_all(bind=engine)

app = FastAPI(title="ERP Backend API", version="1.0.0")


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


class EmployeeCreateRequest(BaseModel):
    name: str = Field(..., min_length=1)
    job_title: str | None = None
    monthly_salary: Decimal | None = None


class EmployeeUpdateRequest(BaseModel):
    name: str | None = None
    job_title: str | None = None
    monthly_salary: Decimal | None = None


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


class SaleLineCreateRequest(BaseModel):
    product_id: int
    quantity: int
    discount_rate: Decimal | None = Decimal("0.00")


class InvoiceCreateRequest(BaseModel):
    customer_id: int
    employee_id: int
    invoice_number: str = Field(..., min_length=1)
    sale_lines: list[SaleLineCreateRequest]


@app.get("/")
def root() -> dict[str, Any]:
    return {"message": "Welcome to the ERP Backend API!"}


@app.get("/health")
def health() -> dict[str, Any]:
    return {"status": "ok"}


@app.get("/customers", response_model=list[dict[str, Any]])
def list_customers(db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    service = CustomerService(db)
    customers = service.list_customers()
    return [
        {
            "id": customer.id,
            "name": customer.name,
            "phone": customer.phone,
            "email": customer.email,
            "address": customer.address,
            "tax_registration_number": customer.tax_registration_number,
        }
        for customer in customers
    ]


@app.post("/customers", status_code=201, response_model=dict[str, Any])
def create_customer(payload: CustomerCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    service = CustomerService(db)
    try:
        customer = service.create_customer(
            name=payload.name,
            phone=payload.phone,
            email=payload.email,
            address=payload.address,
            tax_registration_number=payload.tax_registration_number,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "id": customer.id,
        "name": customer.name,
        "phone": customer.phone,
        "email": customer.email,
        "address": customer.address,
        "tax_registration_number": customer.tax_registration_number,
    }


@app.get("/customers/{customer_id}", response_model=dict[str, Any])
def get_customer(customer_id: int, db: Session = Depends(get_db)) -> dict[str, Any]:
    service = CustomerService(db)
    customer = service.get_customer(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return {
        "id": customer.id,
        "name": customer.name,
        "phone": customer.phone,
        "email": customer.email,
        "address": customer.address,
        "tax_registration_number": customer.tax_registration_number,
    }


@app.put("/customers/{customer_id}", response_model=dict[str, Any])
def update_customer(customer_id: int, payload: CustomerUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    service = CustomerService(db)
    try:
        customer = service.update_customer(
            customer_id=customer_id,
            name=payload.name,
            phone=payload.phone,
            email=payload.email,
            address=payload.address,
            tax_registration_number=payload.tax_registration_number,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "id": customer.id,
        "name": customer.name,
        "phone": customer.phone,
        "email": customer.email,
        "address": customer.address,
        "tax_registration_number": customer.tax_registration_number,
    }


@app.delete("/customers/{customer_id}", status_code=204)
def delete_customer(customer_id: int, db: Session = Depends(get_db)) -> None:
    service = CustomerService(db)
    try:
        service.delete_customer(customer_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/employees", response_model=list[dict[str, Any]])
def list_employees(db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    service = EmployeeService(db)
    employees = service.list_employees()
    return [
        {
            "id": employee.id,
            "name": employee.name,
            "job_title": employee.job_title,
            "monthly_salary": str(employee.monthly_salary),
        }
        for employee in employees
    ]


@app.post("/employees", status_code=201, response_model=dict[str, Any])
def create_employee(payload: EmployeeCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    service = EmployeeService(db)
    try:
        employee = service.create_employee(
            name=payload.name,
            job_title=payload.job_title,
            monthly_salary=payload.monthly_salary,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "id": employee.id,
        "name": employee.name,
        "job_title": employee.job_title,
        "monthly_salary": str(employee.monthly_salary),
    }


@app.get("/employees/{employee_id}", response_model=dict[str, Any])
def get_employee(employee_id: int, db: Session = Depends(get_db)) -> dict[str, Any]:
    service = EmployeeService(db)
    employee = service.get_employee(employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {
        "id": employee.id,
        "name": employee.name,
        "job_title": employee.job_title,
        "monthly_salary": str(employee.monthly_salary),
    }


@app.put("/employees/{employee_id}", response_model=dict[str, Any])
def update_employee(employee_id: int, payload: EmployeeUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    service = EmployeeService(db)
    try:
        employee = service.update_employee(
            employee_id=employee_id,
            name=payload.name,
            job_title=payload.job_title,
            monthly_salary=payload.monthly_salary,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "id": employee.id,
        "name": employee.name,
        "job_title": employee.job_title,
        "monthly_salary": str(employee.monthly_salary),
    }


@app.delete("/employees/{employee_id}", status_code=204)
def delete_employee(employee_id: int, db: Session = Depends(get_db)) -> None:
    service = EmployeeService(db)
    try:
        service.delete_employee(employee_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/products", response_model=list[dict[str, Any]])
def list_products(db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    service = ProductService(db)
    products = service.list_products()
    return [
        {
            "id": product.id,
            "reference": product.reference,
            "name": product.name,
            "description": product.description,
            "unit_price_excl_tax": str(product.unit_price_excl_tax),
            "tax_rate": str(product.tax_rate),
            "stock_quantity": product.stock_quantity,
        }
        for product in products
    ]


@app.post("/products", status_code=201, response_model=dict[str, Any])
def create_product(payload: ProductCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    service = ProductService(db)
    try:
        product = service.create_product(
            reference=payload.reference,
            name=payload.name,
            description=payload.description,
            unit_price_excl_tax=payload.unit_price_excl_tax,
            tax_rate=payload.tax_rate,
            stock_quantity=payload.stock_quantity,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "id": product.id,
        "reference": product.reference,
        "name": product.name,
        "description": product.description,
        "unit_price_excl_tax": str(product.unit_price_excl_tax),
        "tax_rate": str(product.tax_rate),
        "stock_quantity": product.stock_quantity,
    }


@app.get("/products/{product_id}", response_model=dict[str, Any])
def get_product(product_id: int, db: Session = Depends(get_db)) -> dict[str, Any]:
    service = ProductService(db)
    product = service.get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        "id": product.id,
        "reference": product.reference,
        "name": product.name,
        "description": product.description,
        "unit_price_excl_tax": str(product.unit_price_excl_tax),
        "tax_rate": str(product.tax_rate),
        "stock_quantity": product.stock_quantity,
    }


@app.put("/products/{product_id}", response_model=dict[str, Any])
def update_product(product_id: int, payload: ProductUpdateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    service = ProductService(db)
    try:
        product = service.update_product(
            product_id=product_id,
            reference=payload.reference,
            name=payload.name,
            description=payload.description,
            unit_price_excl_tax=payload.unit_price_excl_tax,
            tax_rate=payload.tax_rate,
            stock_quantity=payload.stock_quantity,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "id": product.id,
        "reference": product.reference,
        "name": product.name,
        "description": product.description,
        "unit_price_excl_tax": str(product.unit_price_excl_tax),
        "tax_rate": str(product.tax_rate),
        "stock_quantity": product.stock_quantity,
    }


@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)) -> None:
    service = ProductService(db)
    try:
        service.delete_product(product_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@app.get("/invoices", response_model=list[dict[str, Any]])
def list_invoices(db: Session = Depends(get_db)) -> list[dict[str, Any]]:
    service = InvoiceService(db)
    invoices = service.list_invoices()
    return [
        {
            "id": invoice.id,
            "invoice_number": invoice.invoice_number,
            "invoice_type": invoice.invoice_type,
            "status": invoice.status,
            "invoice_date": invoice.invoice_date.isoformat(),
            "customer_id": invoice.customer_id,
            "employee_id": invoice.employee_id,
        }
        for invoice in invoices
    ]


@app.post("/invoices", status_code=201, response_model=dict[str, Any])
def create_invoice(payload: InvoiceCreateRequest, db: Session = Depends(get_db)) -> dict[str, Any]:
    service = InvoiceService(db)
    try:
        invoice = service.create_invoice(
            customer_id=payload.customer_id,
            employee_id=payload.employee_id,
            invoice_number=payload.invoice_number,
            sale_lines_data=[
                {"product_id": line.product_id, "quantity": line.quantity, "discount_rate": line.discount_rate}
                for line in payload.sale_lines
            ],
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "id": invoice.id,
        "invoice_number": invoice.invoice_number,
        "invoice_type": invoice.invoice_type,
        "status": invoice.status,
        "invoice_date": invoice.invoice_date.isoformat(),
        "customer_id": invoice.customer_id,
        "employee_id": invoice.employee_id,
    }


@app.get("/invoices/{invoice_id}", response_model=dict[str, Any])
def get_invoice(invoice_id: int, db: Session = Depends(get_db)) -> dict[str, Any]:
    service = InvoiceService(db)
    invoice = service.get_invoice(invoice_id)
    if invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return {
        "id": invoice.id,
        "invoice_number": invoice.invoice_number,
        "invoice_type": invoice.invoice_type,
        "status": invoice.status,
        "invoice_date": invoice.invoice_date.isoformat(),
        "customer_id": invoice.customer_id,
        "employee_id": invoice.employee_id,
    }
