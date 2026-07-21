from database.database import Base, engine

from services.customer_service import create_customer, list_customers
from services.employee_service import create_employee, list_employees
from services.product_service import create_product, list_products
from services.invoice_service import create_invoice, list_invoices


def print_menu():
    print("\n" + "=" * 50)
    print("ERP Backend")
    print("=" * 50)
    print("1. Create Product")
    print("2. List Products")
    print("3. Create Customer")
    print("4. List Customers")
    print("5. Create Employee")
    print("6. List Employees")
    print("7. Create Invoice")
    print("8. List Invoices")
    print("0. Exit")


def main():
    Base.metadata.create_all(engine)

    while True:
        print_menu()

        choice = input("\nChoice: ").strip()

        match choice:
            case "1":
                create_product()

            case "2":
                list_products()

            case "3":
                create_customer()

            case "4":
                list_customers()

            case "5":
                create_employee()

            case "6":
                list_employees()

            case "7":
                create_invoice()

            case "8":
                list_invoices()

            case "0":
                print("Goodbye!")
                break

            case _:
                print("Invalid choice.")


if __name__ == "__main__":
    main()