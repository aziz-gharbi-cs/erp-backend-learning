from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from core.security import hash_password, verify_password
from models.employee import Employee
from repositories.employee_repository import EmployeeRepository
from schemas.auth_schema import RegisterRequest


class AuthService:

    def __init__(self, session: Session):
        self.session = session
        self.employee_repo = EmployeeRepository(session)

    def register(self, request: RegisterRequest) -> Employee:

        existing_employee = self.employee_repo.get_by_username(
            request.username
        )

        if existing_employee:
            raise ValueError("Username already exists.")

        employee = Employee(
            username=request.username,
            password_hash=hash_password(request.password),
            name=request.name,
            email=request.email,
            phone_number=request.phone_number,
            address=request.address,
            job_title=request.job_title,
            role=request.role,
        )

        try:

            self.employee_repo.save(employee)

            self.session.commit()

            self.session.refresh(employee)

            return employee

        except IntegrityError:

            self.session.rollback()

            raise ValueError("Employee already exists.")

        except Exception:

            self.session.rollback()

            raise

    def authenticate(
        self,
        username: str,
        password: str,
    ) -> Employee:

        employee = self.employee_repo.get_by_username(username)

        if employee is None:
            raise ValueError("Invalid username or password.")

        if not employee.is_active:
            raise ValueError("Employee account is disabled.")

        if not verify_password(
            password,
            employee.password_hash,
        ):
            raise ValueError("Invalid username or password.")

        return employee