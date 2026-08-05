from decimal import Decimal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.employee import Employee
from repositories.employee_repository import EmployeeRepository


class EmployeeService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = EmployeeRepository(session)

    def create_employee(
        self,
        name: str,
        job_title: str | None = None,
        monthly_salary: Decimal | None = None,
    ) -> Employee:
        """
        Creates a new employee after validating business rules.
        """

        if not name or not name.strip():
            raise ValueError("Employee name cannot be empty.")

        if monthly_salary is not None and monthly_salary < 0:
            raise ValueError("Monthly salary cannot be negative.")

        employee = Employee(
            name=name.strip(),
            job_title=job_title.strip() if job_title else None,
            monthly_salary=monthly_salary,
        )

        try:
            self.repo.save(employee)
            self.session.commit()
            return employee

        except IntegrityError as exc:
            self.session.rollback()
            raise ValueError(
                "An employee with this name already exists."
            ) from exc

        except Exception:
            self.session.rollback()
            raise

    def list_employees(self) -> list[Employee]:
        return self.repo.get_all()

    def get_employee(self, employee_id: int) -> Employee | None:
        return self.repo.get_by_id(employee_id)

    def update_employee(
        self,
        employee_id: int,
        name: str | None = None,
        job_title: str | None = None,
        monthly_salary: Decimal | None = None,
    ) -> Employee:
        employee = self.repo.get_by_id(employee_id)
        if employee is None:
            raise ValueError("Employee not found.")

        if name is not None:
            if not name.strip():
                raise ValueError("Employee name cannot be empty.")
            employee.name = name.strip()

        if job_title is not None:
            employee.job_title = job_title.strip() if job_title else None

        if monthly_salary is not None:
            if monthly_salary < 0:
                raise ValueError("Monthly salary cannot be negative.")
            employee.monthly_salary = monthly_salary

        try:
            self.repo.update(employee)
            self.session.commit()
            return employee
        except IntegrityError as exc:
            self.session.rollback()
            raise ValueError(
                "An employee with this name already exists."
            ) from exc
        except Exception:
            self.session.rollback()
            raise

    def delete_employee(self, employee_id: int) -> None:
        employee = self.repo.get_by_id(employee_id)
        if employee is None:
            raise ValueError("Employee not found.")

        try:
            self.repo.delete(employee)
            self.session.commit()
        except Exception:
            self.session.rollback()
            raise