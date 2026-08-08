from decimal import Decimal

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.employee import Employee, EmployeeRole
from repositories.employee_repository import EmployeeRepository


class EmployeeService:
    def __init__(self, session: Session):
        self.session = session
        self.repo = EmployeeRepository(session)

    def create_employee(
        self,
        name: str,
        username: str,
        password: str,
        job_title: str | None = None,
        monthly_salary: Decimal | None = None,
        is_active: bool = True,
        role: EmployeeRole = EmployeeRole.EMPLOYEE,
    ) -> Employee:
        """
        Creates a new employee after validating business rules.
        """

        if not name or not name.strip():
            raise ValueError("Employee name cannot be empty.")

        if not username or not username.strip():
            raise ValueError("Username cannot be empty.")

        if not password or not password.strip():
            raise ValueError("Password cannot be empty.")

        if monthly_salary is not None and monthly_salary < 0:
            raise ValueError("Monthly salary cannot be negative.")

        # TODO: hash password in the JWT milestone.
        employee = Employee(
            name=name.strip(),
            username=username.strip(),
            password_hash=password.strip(),
            job_title=job_title.strip() if job_title else None,
            monthly_salary=monthly_salary,
            is_active=is_active,
            role=role,
        )

        try:
            self.repo.save(employee)
            self.session.commit()
            return employee

        except IntegrityError as exc:
            self.session.rollback()
            raise ValueError(
                "An employee with this username already exists."
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
        username: str | None = None,
        password: str | None = None,
        job_title: str | None = None,
        monthly_salary: Decimal | None = None,
        is_active: bool | None = None,
        role: EmployeeRole | None = None,
    ) -> Employee:
        employee = self.repo.get_by_id(employee_id)
        if employee is None:
            raise ValueError("Employee not found.")

        if name is not None:
            if not name.strip():
                raise ValueError("Employee name cannot be empty.")
            employee.name = name.strip()

        if username is not None:
            if not username.strip():
                raise ValueError("Username cannot be empty.")
            employee.username = username.strip()

        if password is not None:
            if not password.strip():
                raise ValueError("Password cannot be empty.")
            # TODO: hash password in the JWT milestone.
            employee.password_hash = password.strip()

        if job_title is not None:
            employee.job_title = job_title.strip() if job_title else None

        if monthly_salary is not None:
            if monthly_salary < 0:
                raise ValueError("Monthly salary cannot be negative.")
            employee.monthly_salary = monthly_salary

        if is_active is not None:
            employee.is_active = is_active

        if role is not None:
            employee.role = role

        try:
            self.repo.update(employee)
            self.session.commit()
            return employee
        except IntegrityError as exc:
            self.session.rollback()
            raise ValueError(
                "An employee with this username already exists."
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