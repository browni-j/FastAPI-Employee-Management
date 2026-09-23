from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeUpdate


def create_employee(db: Session, employee: EmployeeCreate):
    normalized_email = employee.email.strip().lower()

    existing_employee = (
        db.query(Employee)
        .filter(func.lower(Employee.email) == normalized_email)
        .first()
    )

    if existing_employee:
        return "duplicate_email"

    db_employee = Employee(
        name=employee.name.strip(),
        email=normalized_email,
        department=employee.department.strip(),
        primary_skill=employee.primary_skill.strip(),
        location=employee.location.strip(),
        work_mode=employee.work_mode,
        is_active=employee.is_active,
    )

    try:
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee

    except IntegrityError:
        db.rollback()
        return "duplicate_email"

    except Exception:
        db.rollback()
        raise


def get_all_employees(
    db: Session,
    search: str | None = None,
    department: str | None = None,
    work_mode: str | None = None,
    is_active: bool | None = None,
    limit: int = 10,
    offset: int = 0,
):
    query = db.query(Employee)

    if search:
        query = query.filter(Employee.name.ilike(f"%{search.strip()}%"))

    if department:
        query = query.filter(
            func.lower(Employee.department) == department.strip().lower()
        )

    if work_mode:
        query = query.filter(Employee.work_mode == work_mode)

    if is_active is not None:
        query = query.filter(Employee.is_active == is_active)

    total = query.count()

    employees = (
        query
        .order_by(Employee.id.asc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": employees,
    }


def get_employee_by_id(db: Session, employee_id: int):
    return (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )


def update_employee(
    db: Session,
    employee_id: int,
    employee: EmployeeUpdate
):
    db_employee = get_employee_by_id(db, employee_id)

    if db_employee is None:
        return None

    normalized_email = employee.email.strip().lower()

    existing_employee = (
        db.query(Employee)
        .filter(
            func.lower(Employee.email) == normalized_email,
            Employee.id != employee_id
        )
        .first()
    )

    if existing_employee:
        return "duplicate_email"

    db_employee.name = employee.name.strip()
    db_employee.email = normalized_email
    db_employee.department = employee.department.strip()
    db_employee.primary_skill = employee.primary_skill.strip()
    db_employee.location = employee.location.strip()
    db_employee.work_mode = employee.work_mode
    db_employee.is_active = employee.is_active

    # created_at is intentionally NOT changed

    try:
        db.commit()
        db.refresh(db_employee)
        return db_employee

    except IntegrityError:
        db.rollback()
        return "duplicate_email"

    except Exception:
        db.rollback()
        raise


def delete_employee(db: Session, employee_id: int):
    db_employee = get_employee_by_id(db, employee_id)

    if db_employee is None:
        return None

    deleted_employee = {
        "id": db_employee.id,
        "name": db_employee.name,
        "email": db_employee.email,
        "department": db_employee.department,
        "primary_skill": db_employee.primary_skill,
        "location": db_employee.location,
        "work_mode": db_employee.work_mode,
        "is_active": db_employee.is_active,
        "created_at": db_employee.created_at,
    }

    try:
        db.delete(db_employee)
        db.commit()
        return deleted_employee

    except Exception:
        db.rollback()
        raise