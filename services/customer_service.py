from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.customer import Customer
from repositories.customer_repository import CustomerRepository


class CustomerService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = CustomerRepository(session)

    def create_customer(
        self,
        name: str,
        phone: str,
        email: str | None = None,
        address: str | None = None,
        tax_registration_number: str | None = None,
    ) -> Customer:
        """
        Creates a new customer after validating business rules.
        """

        if not name or not name.strip():
            raise ValueError("Customer name cannot be empty.")

        if not phone or not phone.strip():
            raise ValueError("Phone number cannot be empty.")

        customer = Customer(
            name=name.strip(),
            phone=phone.strip(),
            email=email.strip() if email else None,
            address=address.strip() if address else None,
            tax_registration_number=(
                tax_registration_number.strip()
                if tax_registration_number
                else None
            ),
        )

        try:
            self.repo.save(customer)
            self.session.commit()
            return customer

        except IntegrityError as exc:
            self.session.rollback()
            raise ValueError(
                "A customer with the same unique information already exists."
            ) from exc

        except Exception:
            self.session.rollback()
            raise

    def list_customers(self) -> list[Customer]:
        return self.repo.get_all()

    def get_customer(self, customer_id: int) -> Customer | None:
        return self.repo.get_by_id(customer_id)

    def update_customer(
        self,
        customer_id: int,
        name: str | None = None,
        phone: str | None = None,
        email: str | None = None,
        address: str | None = None,
        tax_registration_number: str | None = None,
    ) -> Customer:
        customer = self.repo.get_by_id(customer_id)
        if customer is None:
            raise ValueError("Customer not found.")

        if name is not None:
            if not name.strip():
                raise ValueError("Customer name cannot be empty.")
            customer.name = name.strip()

        if phone is not None:
            if not phone.strip():
                raise ValueError("Phone number cannot be empty.")
            customer.phone = phone.strip()

        if email is not None:
            customer.email = email.strip() if email else None

        if address is not None:
            customer.address = address.strip() if address else None

        if tax_registration_number is not None:
            customer.tax_registration_number = (
                tax_registration_number.strip()
                if tax_registration_number
                else None
            )

        try:
            self.repo.update(customer)
            self.session.commit()
            return customer
        except IntegrityError as exc:
            self.session.rollback()
            raise ValueError(
                "A customer with the same unique information already exists."
            ) from exc
        except Exception:
            self.session.rollback()
            raise

    def delete_customer(self, customer_id: int) -> None:
        customer = self.repo.get_by_id(customer_id)
        if customer is None:
            raise ValueError("Customer not found.")

        try:
            self.repo.delete(customer)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise
