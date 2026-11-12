

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from .database import engine, get_db, Base
from .models import Employee
from .schemas import EmployeeCreate, EmployeeResponse
from .services import create_employee, get_employees

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Service",
    description="Microservice for Employee Management",
    version="1.0.0"
)


@app.get("/health")
def health_check():
    return {"status": "Employee Service is running"}


@app.post("/employees", response_model=EmployeeResponse, status_code=201)
def add_employee(employee: EmployeeCreate, db: Session = Depends(get_db)):
    try:
        return create_employee(db, employee)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@app.get("/employees", response_model=list[EmployeeResponse])
def list_employees(db: Session = Depends(get_db)):
    return get_employees(db)


@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def employee_details(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee
