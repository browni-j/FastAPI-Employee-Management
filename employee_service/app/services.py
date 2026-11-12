from sqlalchemy.orm import Session
from sqlalchemy import func

from .models import Employee
from .schemas import EmployeeCreate


def create_employee(db: Session, employee: EmployeeCreate):
    normalized_email = employee.email.strip().lower()

    existing_employee = db.query(Employee).filter(
        func.lower(Employee.email) == normalized_email
    ).first()

    if existing_employee:
        raise ValueError("Email already exists")

    db_employee = Employee(
        name=employee.name,
        email=normalized_email,
        department=employee.department,
        primary_skill=employee.primary_skill,
        location=employee.location,
        work_mode=employee.work_mode,
        is_active=employee.is_active
    )

    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)

    return db_employee


def get_employees(db: Session):
    return db.query(Employee).order_by(Employee.id).all()
