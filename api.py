from typing import Any

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database.database import get_db
from schemas.customer_schema import (
    CustomerCreateRequest,
    CustomerResponse,
    CustomerUpdateRequest,
)
from schemas.employee_schema import (
    EmployeeCreateRequest,
    EmployeeResponse,
    EmployeeUpdateRequest,
)
from schemas.invoice_schema import (
    InvoiceCreateRequest,
    InvoiceResponse,
)
from schemas.product_schema import (
    ProductCreateRequest,
    ProductResponse,
    ProductUpdateRequest,
)
from services.customer_service import CustomerService
from services.employee_service import EmployeeService
from services.invoice_service import InvoiceService
from services.product_service import ProductService

app = FastAPI(title="ERP Backend API", version="1.0.0")


def _service_error_response(exc: ValueError) -> None:
    message = str(exc)
    if "not found" in message.lower():
        raise HTTPException(status_code=404, detail=message) from exc
    raise HTTPException(status_code=400, detail=message) from exc


@app.get("/", response_model=dict[str, Any])
def root() -> dict[str, Any]:
    return {"message": "Welcome to the ERP Backend API!"}


@app.get("/health", response_model=dict[str, Any])
def health() -> dict[str, Any]:
    return {"status": "ok"}


@app.get("/customers", response_model=list[CustomerResponse])
def list_customers(db: Session = Depends(get_db)) -> list[CustomerResponse]:
    service = CustomerService(db)
    customers = service.list_customers()
    return [
        CustomerResponse(
            id=customer.id,
            name=customer.name,
            phone=customer.phone,
            email=customer.email,
            address=customer.address,
            tax_registration_number=customer.tax_registration_number,
        )
        for customer in customers
    ]


@app.post("/customers", status_code=201, response_model=CustomerResponse)
def create_customer(payload: CustomerCreateRequest, db: Session = Depends(get_db)) -> CustomerResponse:
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
        _service_error_response(exc)
    return CustomerResponse(
        id=customer.id,
        name=customer.name,
        phone=customer.phone,
        email=customer.email,
        address=customer.address,
        tax_registration_number=customer.tax_registration_number,
    )


@app.get("/customers/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session = Depends(get_db)) -> CustomerResponse:
    service = CustomerService(db)
    customer = service.get_customer(customer_id)
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    return CustomerResponse(
        id=customer.id,
        name=customer.name,
        phone=customer.phone,
        email=customer.email,
        address=customer.address,
        tax_registration_number=customer.tax_registration_number,
    )


@app.put("/customers/{customer_id}", response_model=CustomerResponse)
def update_customer(customer_id: int, payload: CustomerUpdateRequest, db: Session = Depends(get_db)) -> CustomerResponse:
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
        _service_error_response(exc)
    return CustomerResponse(
        id=customer.id,
        name=customer.name,
        phone=customer.phone,
        email=customer.email,
        address=customer.address,
        tax_registration_number=customer.tax_registration_number,
    )


@app.delete("/customers/{customer_id}", status_code=204)
def delete_customer(customer_id: int, db: Session = Depends(get_db)) -> None:
    service = CustomerService(db)
    try:
        service.delete_customer(customer_id)
    except ValueError as exc:
        _service_error_response(exc)


@app.get("/employees", response_model=list[EmployeeResponse])
def list_employees(db: Session = Depends(get_db)) -> list[EmployeeResponse]:
    service = EmployeeService(db)
    employees = service.list_employees()
    return [
        EmployeeResponse(
            id=employee.id,
            name=employee.name,
            job_title=employee.job_title,
            monthly_salary=employee.monthly_salary,
        )
        for employee in employees
    ]


@app.post("/employees", status_code=201, response_model=EmployeeResponse)
def create_employee(payload: EmployeeCreateRequest, db: Session = Depends(get_db)) -> EmployeeResponse:
    service = EmployeeService(db)
    try:
        employee = service.create_employee(
            name=payload.name,
            job_title=payload.job_title,
            monthly_salary=payload.monthly_salary,
        )
    except ValueError as exc:
        _service_error_response(exc)
    return EmployeeResponse(
        id=employee.id,
        name=employee.name,
        job_title=employee.job_title,
        monthly_salary=employee.monthly_salary,
    )


@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int, db: Session = Depends(get_db)) -> EmployeeResponse:
    service = EmployeeService(db)
    employee = service.get_employee(employee_id)
    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return EmployeeResponse(
        id=employee.id,
        name=employee.name,
        job_title=employee.job_title,
        monthly_salary=employee.monthly_salary,
    )


@app.put("/employees/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int, payload: EmployeeUpdateRequest, db: Session = Depends(get_db)) -> EmployeeResponse:
    service = EmployeeService(db)
    try:
        employee = service.update_employee(
            employee_id=employee_id,
            name=payload.name,
            job_title=payload.job_title,
            monthly_salary=payload.monthly_salary,
        )
    except ValueError as exc:
        _service_error_response(exc)
    return EmployeeResponse(
        id=employee.id,
        name=employee.name,
        job_title=employee.job_title,
        monthly_salary=employee.monthly_salary,
    )


@app.delete("/employees/{employee_id}", status_code=204)
def delete_employee(employee_id: int, db: Session = Depends(get_db)) -> None:
    service = EmployeeService(db)
    try:
        service.delete_employee(employee_id)
    except ValueError as exc:
        _service_error_response(exc)


@app.get("/products", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)) -> list[ProductResponse]:
    service = ProductService(db)
    products = service.list_products()
    return [
        ProductResponse(
            id=product.id,
            reference=product.reference,
            name=product.name,
            description=product.description,
            unit_price_excl_tax=product.unit_price_excl_tax,
            tax_rate=product.tax_rate,
            stock_quantity=product.stock_quantity,
        )
        for product in products
    ]


@app.post("/products", status_code=201, response_model=ProductResponse)
def create_product(payload: ProductCreateRequest, db: Session = Depends(get_db)) -> ProductResponse:
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
        _service_error_response(exc)
    return ProductResponse(
        id=product.id,
        reference=product.reference,
        name=product.name,
        description=product.description,
        unit_price_excl_tax=product.unit_price_excl_tax,
        tax_rate=product.tax_rate,
        stock_quantity=product.stock_quantity,
    )


@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)) -> ProductResponse:
    service = ProductService(db)
    product = service.get_product(product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse(
        id=product.id,
        reference=product.reference,
        name=product.name,
        description=product.description,
        unit_price_excl_tax=product.unit_price_excl_tax,
        tax_rate=product.tax_rate,
        stock_quantity=product.stock_quantity,
    )


@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, payload: ProductUpdateRequest, db: Session = Depends(get_db)) -> ProductResponse:
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
        _service_error_response(exc)
    return ProductResponse(
        id=product.id,
        reference=product.reference,
        name=product.name,
        description=product.description,
        unit_price_excl_tax=product.unit_price_excl_tax,
        tax_rate=product.tax_rate,
        stock_quantity=product.stock_quantity,
    )


@app.delete("/products/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)) -> None:
    service = ProductService(db)
    try:
        service.delete_product(product_id)
    except ValueError as exc:
        _service_error_response(exc)


@app.get("/invoices", response_model=list[InvoiceResponse])
def list_invoices(db: Session = Depends(get_db)) -> list[InvoiceResponse]:
    service = InvoiceService(db)
    invoices = service.list_invoices()
    return [
        InvoiceResponse(
            id=invoice.id,
            invoice_number=invoice.invoice_number,
            invoice_type=invoice.invoice_type,
            status=invoice.status,
            invoice_date=invoice.invoice_date.isoformat(),
            customer_id=invoice.customer_id,
            employee_id=invoice.employee_id,
        )
        for invoice in invoices
    ]


@app.post("/invoices", status_code=201, response_model=InvoiceResponse)
def create_invoice(payload: InvoiceCreateRequest, db: Session = Depends(get_db)) -> InvoiceResponse:
    service = InvoiceService(db)
    try:
        invoice = service.create_invoice(
            customer_id=payload.customer_id,
            employee_id=payload.employee_id,
            invoice_number=payload.invoice_number,
            sale_lines_data=[
                {
                    "product_id": line.product_id,
                    "quantity": line.quantity,
                    "discount_rate": line.discount_rate,
                }
                for line in payload.sale_lines
            ],
        )
    except ValueError as exc:
        _service_error_response(exc)
    return InvoiceResponse(
        id=invoice.id,
        invoice_number=invoice.invoice_number,
        invoice_type=invoice.invoice_type,
        status=invoice.status,
        invoice_date=invoice.invoice_date.isoformat(),
        customer_id=invoice.customer_id,
        employee_id=invoice.employee_id,
    )


@app.get("/invoices/{invoice_id}", response_model=InvoiceResponse)
def get_invoice(invoice_id: int, db: Session = Depends(get_db)) -> InvoiceResponse:
    service = InvoiceService(db)
    invoice = service.get_invoice(invoice_id)
    if invoice is None:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return InvoiceResponse(
        id=invoice.id,
        invoice_number=invoice.invoice_number,
        invoice_type=invoice.invoice_type,
        status=invoice.status,
        invoice_date=invoice.invoice_date.isoformat(),
        customer_id=invoice.customer_id,
        employee_id=invoice.employee_id,
    )


@app.put("/invoices/{invoice_id}", response_model=InvoiceResponse)
def update_invoice(invoice_id: int, payload: InvoiceCreateRequest, db: Session = Depends(get_db)) -> InvoiceResponse:
    service = InvoiceService(db)
    try:
        invoice = service.update_invoice(
            invoice_id=invoice_id,
            customer_id=payload.customer_id,
            employee_id=payload.employee_id,
            invoice_number=payload.invoice_number,
            sale_lines_data=[
                {
                    "product_id": line.product_id,
                    "quantity": line.quantity,
                    "discount_rate": line.discount_rate,
                }
                for line in payload.sale_lines
            ],
        )
    except ValueError as exc:
        _service_error_response(exc)
    return InvoiceResponse(
        id=invoice.id,
        invoice_number=invoice.invoice_number,
        invoice_type=invoice.invoice_type,
        status=invoice.status,
        invoice_date=invoice.invoice_date.isoformat(),
        customer_id=invoice.customer_id,
        employee_id=invoice.employee_id,
    )


@app.delete("/invoices/{invoice_id}", status_code=204)
def delete_invoice(invoice_id: int, db: Session = Depends(get_db)) -> None:
    service = InvoiceService(db)
    try:
        service.delete_invoice(invoice_id)
    except ValueError as exc:
        _service_error_response(exc)

