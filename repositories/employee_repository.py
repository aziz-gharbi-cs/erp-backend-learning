from sqlalchemy import select
from sqlalchemy.orm import Session

from models.employee import Employee


class EmployeeRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, employee: Employee) -> None:
        self.session.add(employee)
        self.session.flush()

    def get_all(self) -> list[Employee]:
        stmt = select(Employee)
        return list(self.session.scalars(stmt))

    def get_by_id(self, employee_id: int) -> Employee | None:
        stmt = select(Employee).where(Employee.id == employee_id)
        return self.session.scalar(stmt)

    def get_by_name(self, name: str) -> list[Employee]:
        stmt = select(Employee).where(Employee.name == name)
        return list(self.session.scalars(stmt))

    def update(self, employee: Employee) -> None:
        self.session.merge(employee)
        self.session.flush()

    def delete(self, employee: Employee) -> None:
        self.session.delete(employee)
        self.session.flush()