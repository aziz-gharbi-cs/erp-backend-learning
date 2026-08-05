from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.invoice import Invoice
from models.saleline import SaleLine

from repositories.customer_repository import CustomerRepository
from repositories.employee_repository import EmployeeRepository
from repositories.invoice_repository import InvoiceRepository
from repositories.product_repository import ProductRepository


class InvoiceService:
    def __init__(self, session: Session):
        self.session = session
        self.invoice_repo = InvoiceRepository(session)
        self.customer_repo = CustomerRepository(session)
        self.employee_repo = EmployeeRepository(session)
        self.product_repo = ProductRepository(session)

    def create_invoice(
        self,
        customer_id: int,
        employee_id: int,
        invoice_number: str,
        sale_lines_data: list[dict],
    ) -> Invoice:
        """
        Creates a new invoice after validating business rules.
        """

        customer = self.customer_repo.get_by_id(customer_id)
        if customer is None:
            raise ValueError("Customer not found.")

        employee = self.employee_repo.get_by_id(employee_id)
        if employee is None:
            raise ValueError("Employee not found.")

        if not invoice_number or not invoice_number.strip():
            raise ValueError("Invoice number cannot be empty.")

        invoice = Invoice(
            invoice_number=invoice_number.strip(),
            invoice_type="Sale",
            status="Draft",
            customer=customer,
            employee=employee,
        )

        for line_data in sale_lines_data:
            product_id = line_data.get("product_id")
            quantity = line_data.get("quantity")

            product = self.product_repo.get_by_id(product_id)
            if product is None:
                raise ValueError(f"Product with ID {product_id} not found.")

            if quantity <= 0:
                raise ValueError("Quantity must be greater than zero.")

            sale_line = SaleLine(
                product=product,
                product_name=product.name,
                product_description=product.description,
                unit_price_excl_tax=product.unit_price_excl_tax,
                tax_rate=product.tax_rate,
                quantity=quantity,
                discount_rate=line_data.get("discount_rate", 0),
            )

            invoice.sale_lines.append(sale_line)

        if not invoice.sale_lines:
            raise ValueError("An invoice must contain at least one sale line.")

        try:
            self.invoice_repo.save(invoice)
            self.session.commit()
            return invoice

        except IntegrityError as exc:
            self.session.rollback()
            raise ValueError(
                "Could not create invoice due to a database constraint."
            ) from exc

        except Exception:
            self.session.rollback()
            raise

    def list_invoices(self) -> list[Invoice]:
        return self.invoice_repo.get_all()

    def get_invoice(self, invoice_id: int) -> Invoice | None:
        return self.invoice_repo.get_by_id(invoice_id)

    def update_invoice(
        self,
        invoice_id: int,
        customer_id: int | None = None,
        employee_id: int | None = None,
        invoice_number: str | None = None,
        sale_lines_data: list[dict] | None = None,
        invoice_type: str | None = None,
        status: str | None = None,
    ) -> Invoice:
        invoice = self.invoice_repo.get_by_id(invoice_id)
        if invoice is None:
            raise ValueError("Invoice not found.")

        if customer_id is not None:
            customer = self.customer_repo.get_by_id(customer_id)
            if customer is None:
                raise ValueError("Customer not found.")
            invoice.customer = customer
            invoice.customer_id = customer.id

        if employee_id is not None:
            employee = self.employee_repo.get_by_id(employee_id)
            if employee is None:
                raise ValueError("Employee not found.")
            invoice.employee = employee
            invoice.employee_id = employee.id

        if invoice_number is not None:
            invoice_number = invoice_number.strip()
            if not invoice_number:
                raise ValueError("Invoice number cannot be empty.")
            invoice.invoice_number = invoice_number

        if invoice_type is not None:
            invoice.invoice_type = invoice_type

        if status is not None:
            invoice.status = status

        if sale_lines_data is not None:
            invoice.sale_lines.clear()

            for line_data in sale_lines_data:
                product_id = line_data.get("product_id")
                quantity = line_data.get("quantity")

                product = self.product_repo.get_by_id(product_id)
                if product is None:
                    raise ValueError(f"Product with ID {product_id} not found.")

                if quantity <= 0:
                    raise ValueError("Quantity must be greater than zero.")

                sale_line = SaleLine(
                    product=product,
                    product_name=product.name,
                    product_description=product.description,
                    unit_price_excl_tax=product.unit_price_excl_tax,
                    tax_rate=product.tax_rate,
                    quantity=quantity,
                    discount_rate=line_data.get("discount_rate", 0),
                )
                invoice.sale_lines.append(sale_line)

            if not invoice.sale_lines:
                raise ValueError("An invoice must contain at least one sale line.")

        try:
            self.invoice_repo.update(invoice)
            self.session.commit()
            return invoice
        except IntegrityError as exc:
            self.session.rollback()
            raise ValueError(
                "Could not update invoice due to a database constraint."
            ) from exc
        except Exception:
            self.session.rollback()
            raise

    def delete_invoice(self, invoice_id: int) -> None:
        invoice = self.invoice_repo.get_by_id(invoice_id)
        if invoice is None:
            raise ValueError("Invoice not found.")

        try:
            self.invoice_repo.delete(invoice)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise