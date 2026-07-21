from sqlalchemy import select
from sqlalchemy.orm import Session

from models.customer import Customer


class CustomerRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, customer: Customer) -> None:
        self.session.add(customer)
        self.session.flush()

    def get_all(self) -> list[Customer]:
        stmt = select(Customer)
        return list(self.session.scalars(stmt))

    def get_by_id(self, customer_id: int) -> Customer | None:
        stmt = select(Customer).where(Customer.id == customer_id)
        return self.session.scalar(stmt)

    def get_by_name(self, name: str) -> list[Customer]:
        stmt = select(Customer).where(Customer.name == name)
        return list(self.session.scalars(stmt))

    def update(self, customer: Customer) -> None:
        self.session.merge(customer)
        self.session.flush()

    def delete(self, customer: Customer) -> None:
        self.session.delete(customer)
        self.session.flush()