from sqlalchemy.exc import IntegrityError

from database.database import SessionLocal
from models.customer import Customer
from repositories.customer_repository import CustomerRepository


def create_customer():
    with SessionLocal() as session:
        repo = CustomerRepository(session)

        try:
            while True:
                name = input("Customer Name: ").strip()
                if name:
                    break
                print("Customer name cannot be empty.")

            while True:
                phone = input("Phone: ").strip()
                if phone:
                    break
                print("Phone cannot be empty.")

            email = input("Email (optional): ").strip() or None
            address = input("Address (optional): ").strip() or None
            tax_registration_number = (
                input("Tax Registration Number (optional): ").strip() or None
            )

            customer = Customer(
                name=name,
                phone=phone,
                email=email,
                address=address,
                tax_registration_number=tax_registration_number,
            )

            repo.save(customer)

            session.commit()

            return customer

        except IntegrityError:
            session.rollback()
            print("Error: A customer with the same unique information already exists.")

        except Exception:
            session.rollback()
            raise


def list_customers():
    with SessionLocal() as session:
        repo = CustomerRepository(session)
        customers = repo.get_all()

    if not customers:
        print("No customers found.")
        return

    for customer in customers:
        print(customer)