from sqlalchemy.exc import IntegrityError

from database.database import SessionLocal

from models.invoice import Invoice
from models.saleline import SaleLine

from repositories.customer_repository import CustomerRepository
from repositories.employee_repository import EmployeeRepository
from repositories.invoice_repository import InvoiceRepository
from repositories.product_repository import ProductRepository


def create_invoice():
    with SessionLocal() as session:
        invoice_repo = InvoiceRepository(session)
        customer_repo = CustomerRepository(session)
        employee_repo = EmployeeRepository(session)
        product_repo = ProductRepository(session)

        try:
            # ---------- Customer ----------

            while True:
                try:
                    customer_id = int(input("Customer ID: "))
                    break
                except ValueError:
                    print("Invalid customer ID.")

            customer = customer_repo.get_by_id(customer_id)

            if customer is None:
                print("Customer not found.")
                return

            # ---------- Employee ----------

            while True:
                try:
                    employee_id = int(input("Employee ID: "))
                    break
                except ValueError:
                    print("Invalid employee ID.")

            employee = employee_repo.get_by_id(employee_id)

            if employee is None:
                print("Employee not found.")
                return

            # ---------- Invoice ----------

            while True:
                invoice_number = input("Invoice Number: ").strip()

                if invoice_number:
                    break

                print("Invoice number cannot be empty.")

            invoice = Invoice(
                invoice_number=invoice_number,
                invoice_type="Sale",
                status="Draft",
                customer=customer,
                employee=employee,
            )

            # ---------- Sale Lines ----------

            while True:
                product_id_input = input("Product ID (press Enter to finish): ").strip()

                if product_id_input == "":
                    break

                try:
                    product_id = int(product_id_input)
                except ValueError:
                    print("Invalid product ID.")
                    continue

                product = product_repo.get_by_id(product_id)

                if product is None:
                    print("Product not found.")
                    continue

                while True:
                    try:
                        quantity = int(input("Quantity: "))

                        if quantity > 0:
                            break

                        print("Quantity must be greater than zero.")

                    except ValueError:
                        print("Invalid quantity.")

                sale_line = SaleLine(
                    product=product,
                    product_name=product.name,
                    product_description=product.description,
                    unit_price_excl_tax=product.unit_price_excl_tax,
                    tax_rate=product.tax_rate,
                    quantity=quantity,
                    discount_rate=0,
                )

                invoice.sale_lines.append(sale_line)

            if not invoice.sale_lines:
                print("An invoice must contain at least one sale line.")
                return

            invoice_repo.save(invoice)

            session.commit()

            print("Invoice created successfully.")

            return invoice

        except IntegrityError:
            session.rollback()
            print("Could not create invoice due to a database constraint.")

        except Exception:
            session.rollback()
            raise


def list_invoices():
    with SessionLocal() as session:
        repo = InvoiceRepository(session)
        invoices = repo.get_all()

    if not invoices:
        print("No invoices found.")
        return

    for invoice in invoices:
        print("\n" + "=" * 80)
        print(invoice)

        if invoice.sale_lines:
            print("\nSale Lines:")
            for line in invoice.sale_lines:
                print(f"  {line}")

        print("=" * 80)