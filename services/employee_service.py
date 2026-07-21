from decimal import Decimal, InvalidOperation

from sqlalchemy.exc import IntegrityError

from database.database import SessionLocal
from models.employee import Employee
from repositories.employee_repository import EmployeeRepository


def create_employee():
    with SessionLocal() as session:
        repo = EmployeeRepository(session)

        try:
            while True:
                name = input("Employee Name: ").strip()
                if name:
                    break
                print("Employee name cannot be empty.")

            job_title = input("Job Title (optional): ").strip() or None

            while True:
                salary_input = input("Monthly Salary (optional): ").strip()

                if not salary_input:
                    monthly_salary = None
                    break

                try:
                    monthly_salary = Decimal(salary_input)

                    if monthly_salary >= 0:
                        break

                    print("Monthly salary cannot be negative.")

                except InvalidOperation:
                    print("Invalid salary.")

            employee = Employee(
                name=name,
                job_title=job_title,
                monthly_salary=monthly_salary,
            )

            repo.save(employee)

            session.commit()

            print("Employee created successfully.")

            return employee

        except IntegrityError:
            session.rollback()
            print("Error: An employee with the same unique information already exists.")

        except Exception:
            session.rollback()
            raise


def list_employees():
    with SessionLocal() as session:
        repo = EmployeeRepository(session)
        employees = repo.get_all()

    if not employees:
        print("No employees found.")
        return

    for employee in employees:
        print(employee)