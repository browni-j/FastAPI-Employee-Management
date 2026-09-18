from fastapi import Depends, FastAPI, HTTPException, Path, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from app.services import (
    create_employee,
    delete_employee,
    get_all_employees,
    get_employee_by_id,
    update_employee,
)

app = FastAPI()

@app.exception_handler(SQLAlchemyError)
async def database_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={"detail": "Database operation failed"}
    )

Base.metadata.create_all(bind=engine)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/employees", response_model=EmployeeResponse, status_code=201)
def add_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    created_employee = create_employee(db, employee)

    if created_employee == "duplicate_email":
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    return created_employee


@app.get("/employees", response_model=list[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    return get_all_employees(db)


@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def get_employee(
    employee_id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    employee = get_employee_by_id(db, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


@app.put("/employees/{employee_id}", response_model=EmployeeResponse)
def edit_employee(
    employee: EmployeeUpdate,
    employee_id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    updated_employee = update_employee(db, employee_id, employee)

    if updated_employee == "duplicate_email":
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    if updated_employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return updated_employee


@app.delete("/employees/{employee_id}")
def delete_employee_api(
    employee_id: int = Path(gt=0),
    db: Session = Depends(get_db)
):
    deleted_employee = delete_employee(db, employee_id)

    if deleted_employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "message": "Employee deleted successfully",
        "employee": deleted_employee
    };
